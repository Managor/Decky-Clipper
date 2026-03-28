import os
import signal
from datetime import datetime
import subprocess
import asyncio

import decky


class Plugin:
  _process = None
  _env = {**os.environ, "LD_LIBRARY_PATH":"", "XDG_RUNTIME_DIR":"/run/user/1000"}


  # Record the gamescope pipewire node
  async def start_record(self, app_name: str, microphone: bool):
    # Generate a gstreamer pipeline
    gstreamer = f"GST_PLUGIN_PATH={decky.DECKY_PLUGIN_DIR}/bin/gstreamer-1.0 gst-launch-1.0 -v "
    videopipeline = "pipewiresrc do-timestamp=true target-object=gamescope client-name=Video-capture keepalive-time=100 ! queue ! video/x-raw,format=NV12 ! vah264enc ! h264parse ! mux. "
    audiosource = "pipewiresrc do-timestamp=true stream-properties=props,stream.capture.sink=true client-name=Speaker-capture ! queue ! audio/x-raw,channels=2 ! mixer. "
    if microphone:
      audiosource = audiosource + "pipewiresrc do-timestamp=true client-name=Microphone-capture ! queue ! audio/x-raw,channels=2 ! mixer. "
    audioencode = "audiomixer name=mixer ! opusenc ! mux. "
    filename = f"{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}-{app_name}.mkv"
    filecreation = f"matroskamux name=mux ! filesink 'location={decky.HOME}/Videos/{filename}'"

    pipeline = f"{gstreamer}{videopipeline}{audiosource}{audioencode}{filecreation}"

    decky.logger.info("Running pipeline: " + pipeline)
    Plugin._process = subprocess.Popen(pipeline, shell=True, env=self._env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    asyncio.create_task(asyncio.to_thread(self.log_stdout))
    return


  async def stop_record(self):
    decky.logger.info("Stopping recording.")
    decommission = Plugin._process
    Plugin._process = None
    decky.logger.info("Sending signal to terminate.")
    decommission.send_signal(signal.SIGINT)
    try:
      decommission.wait(timeout=2)
    except Exception:
      decky.logger.info("Couldn't terminate. Killing.")
      decommission.kill()
    decky.logger.info("Recording stopped.")
    return


  async def is_recording(self) -> bool:
    return Plugin._process != None


  def log_stdout(self):
    decky.logger.info("Logging stdout")
    for line in Plugin._process.stdout:
      decky.logger.info("STDOUT: " + line.rstrip())
    decky.logger.info("End of stdout")
    return








  # Asyncio-compatible long-running code, executed in a task when the plugin is loaded
  async def _main(self):
    decky.logger.info("Plugin loaded!")
    decky.logger.info("Device variant: " + subprocess.check_output(["atomupd-manager", "tracked-variant"], text=True).rstrip())
    decky.logger.info("Release branch: " + subprocess.check_output(["atomupd-manager", "tracked-branch"], text=True).rstrip())

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
