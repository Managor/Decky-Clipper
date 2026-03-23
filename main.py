import os
import re
import signal
from datetime import datetime
import subprocess

import decky


class Plugin:
  _process = None
  _env = {**os.environ, "LD_LIBRARY_PATH":"", "XDG_RUNTIME_DIR":"/run/user/1000"}

  # Record the gamescope pipewire node
  async def start_record(self, app_name: str, microphone: bool):
    # Guard against starting a second recording while one is already running
    if Plugin._process is not None:
      decky.logger.warning("Recording already in progress, ignoring start request.")
      return

    # Ensure the Videos directory exists
    videos_dir = f"{decky.HOME}/Videos"
    os.makedirs(videos_dir, exist_ok=True)

    # Sanitize app_name to prevent shell injection and filename issues
    safe_app_name = re.sub(r"[^\w\-.]", "_", app_name)

    # Generate a gstreamer pipeline
    gstreamer = f"GST_PLUGIN_PATH={decky.DECKY_PLUGIN_DIR}/bin/gstreamer-1.0 gst-launch-1.0 "
    videopipeline = "pipewiresrc do-timestamp=true target-object=gamescope client-name=Video-capture ! videoconvert ! vah264enc ! h264parse ! mux. "
    audiosource = "pipewiresrc do-timestamp=true stream-properties=props,stream.capture.sink=true client-name=Speaker-capture ! audio/x-raw,channels=2 ! mixer. "
    if microphone:
      audiosource = audiosource + "pipewiresrc do-timestamp=true client-name=Microphone-capture ! audio/x-raw,channels=2 ! mixer. "
    audioencode = "audiomixer name=mixer ! opusenc ! mux. "
    filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}-{safe_app_name}.mkv"
    filecreation = f"matroskamux name=mux ! filesink location={videos_dir}/{filename}"

    pipeline = f"{gstreamer}{videopipeline}{audiosource}{audioencode}{filecreation}"

    decky.logger.info("Running pipeline: " + pipeline)
    Plugin._process = subprocess.Popen(
      pipeline,
      shell=True,
      env=self._env,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,  # Capture stderr separately from stdout
      text=True
    )

  async def stop_record(self):
    # Guard against stopping when nothing is recording
    if Plugin._process is None:
      decky.logger.warning("No recording in progress, ignoring stop request.")
      return

    decommission = Plugin._process
    Plugin._process = None
    decky.logger.info("Sending signal to terminate.")
    decommission.send_signal(signal.SIGINT)
    try:
      decommission.wait(timeout=2)
    except Exception:
      decky.logger.info("Couldn't terminate. Killing.")
      decommission.kill()
      decommission.wait()

    for line in decommission.stdout:
      decky.logger.info("stdout: " + line.rstrip())
    for line in decommission.stderr:
      decky.logger.error("stderr: " + line.rstrip())

  async def is_recording(self) -> bool:
    return Plugin._process is not None

  # Asyncio-compatible long-running code, executed in a task when the plugin is loaded
  async def _main(self):
    decky.logger.info("Plugin loaded!")

  # Function called first during the unload process, utilize this to handle your plugin being stopped, but not
  # completely removed
  async def _unload(self):
    # Stop any active recording cleanly before unloading
    if Plugin._process is not None:
      decky.logger.info("Unloading: stopping active recording.")
      await self.stop_record()
    decky.logger.info("Plugin unloaded!")

  # Function called after `_unload` during uninstall, utilize this to clean up processes and other remnants of your
  # plugin that may remain on the system
  async def _uninstall(self):
    decky.logger.info("Plugin uninstalled!")

  # Migrations that should be performed before entering `_main()`.
  async def _migration(self):
    decky.logger.info("Migrating")
