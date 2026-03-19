import os
import asyncio
import time
import signal

import subprocess
import decky


class Plugin:
  _process = None
  _env = {**os.environ, "LD_LIBRARY_PATH":"", "XDG_RUNTIME_DIR":"/run/user/1000"}
  # Record the gamescope pipewire node
  async def start_record(self):
    gstpluginspath = decky.DECKY_PLUGIN_DIR + "/bin/gstreamer-1.0"

    filesinklocation = decky.HOME + "/Videos/test.mkv"
    pipeline = f"GST_PLUGIN_PATH={gstpluginspath} gst-launch-1.0 -ev pipewiresrc do-timestamp=true target-object=gamescope keepalive-time=33 ! videoconvert ! vah264enc ! h264parse ! mux. pipewiresrc do-timestamp=true ! opusenc ! matroskamux name=mux ! filesink location={filesinklocation}"

    decky.logger.info("Running pipeline: " + pipeline)
    process = subprocess.Popen(pipeline, shell=True, env=self._env)

    decky.logger.info("Sending signal to terminate.")
    time.sleep(3)
    process.send_signal(signal.SIGINT)
    try:
      process.wait(timeout=3)
    except Exception:
      decky.logger.info("Couldn't terminate. Killing.")
      process.kill()





  # Asyncio-compatible long-running code, executed in a task when the plugin is loaded
  async def _main(self):
      self.loop = asyncio.get_event_loop()
      decky.logger.info("Hello World!")

  # Function called first during the unload process, utilize this to handle your plugin being stopped, but not
  # completely removed
  async def _unload(self):
      decky.logger.info("Goodnight World!")
      pass

  # Function called after `_unload` during uninstall, utilize this to clean up processes and other remnants of your
  # plugin that may remain on the system
  async def _uninstall(self):
      decky.logger.info("Goodbye World!")
      pass

  # Migrations that should be performed before entering `_main()`.
  async def _migration(self):
      decky.logger.info("Migrating")
      # Here's a migration example for logs:
      # - `~/.config/decky-template/template.log` will be migrated to `decky.decky_LOG_DIR/template.log`
      decky.migrate_logs(os.path.join(decky.DECKY_USER_HOME,
                                              ".config", "decky-template", "template.log"))
      # Here's a migration example for settings:
      # - `~/homebrew/settings/template.json` is migrated to `decky.decky_SETTINGS_DIR/template.json`
      # - `~/.config/decky-template/` all files and directories under this root are migrated to `decky.decky_SETTINGS_DIR/`
      decky.migrate_settings(
          os.path.join(decky.DECKY_HOME, "settings", "template.json"),
          os.path.join(decky.DECKY_USER_HOME, ".config", "decky-template"))
      # Here's a migration example for runtime data:
      # - `~/homebrew/template/` all files and directories under this root are migrated to `decky.decky_RUNTIME_DIR/`
      # - `~/.local/share/decky-template/` all files and directories under this root are migrated to `decky.decky_RUNTIME_DIR/`
      decky.migrate_runtime(
          os.path.join(decky.DECKY_HOME, "template"),
          os.path.join(decky.DECKY_USER_HOME, ".local", "share", "decky-template"))
