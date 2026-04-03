import {
  ButtonItem,
  PanelSection,
  ToggleField,
  staticClasses,
  Navigation,
  Router,
  showModal,
  ModalRoot,
  Focusable,
  DialogButtonPrimary,
  DialogButtonSecondary,
} from "@decky/ui";
import {
  callable,
  definePlugin,
} from "@decky/api"
import { useEffect, useState } from "react";
import { FaCameraRetro } from "react-icons/fa";

const startRecord = callable<[string, boolean], void>("start_record");
const stopRecord = callable("stop_record");
const checkRecordingState = callable<[], boolean>("is_recording")
const listFiles = callable<[], string[]>("list_files")


function Content() {
  const [isRecording, setIsRecording] = useState(false);
  const [useMicrophone, setUseMicrophone] = useState(false);
  // const [files, setFiles] = useState<string[]>([]);
  const files = [ "testfile.mkv" ]
  const playing = true

  const togglePlayback = async () => {

  }

  const seek = async (seconds: number) => {

  }

  const initiateRecording = async () => {
    if (!isRecording) {
      await startRecord(Router.MainRunningApp?.display_name ?? "Steam", useMicrophone);
      Navigation.CloseSideMenus();
    } else {
      await stopRecord();
    }
    setIsRecording(await checkRecordingState());
  };

  useEffect(() => {
    (async () => {
      setIsRecording(await checkRecordingState())
      // setFiles(await listFiles())
    })();
  }, []);

  const playVideo = async (file: string) => {
    showModal(
      <ModalRoot>
        <div>
          {file}
        </div>
        <video
          src={`http://localhost:8000/${file}`}
          // controls
          autoPlay
          style={{
            width: "100%",
            borderRadius: "6px",
            background: "#000",
            maxHeight: "60vh",
          }}
        />
        <Focusable style={{ display: "flex", justifyContent: "flex-end", gap: "1em" }}>
          <DialogButtonPrimary onClick={togglePlayback}>{playing ? "Pause" : "Play"}</DialogButtonPrimary>
          <DialogButtonSecondary onClick={() => seek(-10)}>Rewind 10s</DialogButtonSecondary>
          <DialogButtonSecondary onClick={() => seek(10)}>Forward 10s</DialogButtonSecondary>
        </Focusable>
      </ModalRoot>
    );
  };

  return (
    <PanelSection>
      <ButtonItem label="The recording will be saved in ~/Videos/ with the current timestamp" layout="below" onClick={initiateRecording} >
        {isRecording ? "Stop recording" : "Start recording"}
      </ButtonItem>
      <ToggleField  label="Record microphone" checked={useMicrophone} onChange={(e) => setUseMicrophone(e)}></ToggleField>
      {files.map((file) => (
        <ButtonItem onClick={() => playVideo(file)} bottomSeparator="none" layout="below">
          {file}
        </ButtonItem>
      ))}
    </PanelSection>
  );
};

export default definePlugin(() => {
  return {
    name: "Decky Clipper",
    titleView: <div className={staticClasses.Title}>Decky Clipper</div>,
    content: <Content />,
    icon: <FaCameraRetro />,
    onDismount() {},
  };
});
