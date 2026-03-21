import os
import signal
from datetime import datetime
import subprocess

import decky


class Plugin:
  _process = None
  _env = {**os.environ, "LD_LIBRARY_PATH":"", "XDG_RUNTIME_DIR":"/run/user/1000"}
  # Record the gamescope pipewire node
  async def start_record(self, app_name):
    # Generate a gstreamer pipeline
    gstpluginspath = f"GST_PLUGIN_PATH={decky.DECKY_PLUGIN_DIR}/bin/gstreamer-1.0"
    videopipeline = "pipewiresrc do-timestamp=true target-object=gamescope ! videoconvert ! vah264enc ! h264parse ! mux."
    audiopipeline = "pipewiresrc do-timestamp=true stream-properties=props,stream.capture.sink=true ! opusenc"
    filename = f"{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}-{app_name}.mkv"
    filecreationpipeline = f"matroskamux name=mux ! filesink location={decky.HOME}/Videos/{filename}"

    pipeline = f"{gstpluginspath} gst-launch-1.0 {videopipeline} {audiopipeline} ! {filecreationpipeline}"

    decky.logger.info("Running pipeline: " + pipeline)
    Plugin._process = subprocess.Popen(pipeline, shell=True, env=self._env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return

  async def stop_record(self):
    decommission = Plugin._process
    Plugin._process = None
    decky.logger.info("Sending signal to terminate.")
    decommission.send_signal(signal.SIGINT)
    try:
      decommission.wait(timeout=2)
    except Exception:
      decky.logger.info("Couldn't terminate. Killing.")
      decommission.kill()

    for line in decommission.stdout:
      decky.logger.info("stdout: " + line)
    return

  async def is_recording(self) -> bool:
    return Plugin._process != None







  # Asyncio-compatible long-running code, executed in a task when the plugin is loaded
  async def _main(self):
    decky.logger.info("Plugin loaded!")

  # Function called first during the unload process, utilize this to handle your plugin being stopped, but not
  # completely removed
  async def _unload(self):
    # Ensure that there are no detached processes
    subprocess.run(["killall", "gst-launch-1.0"])
    decky.logger.info("Plugin unloaded!")

  # Function called after `_unload` during uninstall, utilize this to clean up processes and other remnants of your
  # plugin that may remain on the system
  async def _uninstall(self):
    decky.logger.info("Plugin uninstalled!")

  # Migrations that should be performed before entering `_main()`.
  async def _migration(self):
    decky.logger.info("Migrating")
