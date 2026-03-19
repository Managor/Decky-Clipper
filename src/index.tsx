import {
  ButtonItem,
  PanelSection,
  PanelSectionRow,
  staticClasses,
} from "@decky/ui";
import {
  callable,
  definePlugin,
} from "@decky/api"
import { useEffect, useState } from "react";
import { FaCameraRetro } from "react-icons/fa";

const startRecord = callable("start_record");
const stopRecord = callable("stop_record");
const checkRecordingState = callable<[], boolean>("is_recording")


function Content() {
  const [isRecording, setIsRecording] = useState(false);


  const onClick = async () => {
    if (!isRecording) {
      await startRecord();
    } else {
      await stopRecord();
    }
    setIsRecording(await checkRecordingState());
  };

  useEffect(() => {
    (async () => {
      setIsRecording(await checkRecordingState())
    })();
  }, []);

  return (
    <PanelSection>
      <PanelSectionRow>
        <ButtonItem label="The recording will be saved in ~/Videos/ with the current timestamp" layout="below" onClick={onClick} >
          {isRecording ? "Stop recording" : "Start recording"}
        </ButtonItem>
      </PanelSectionRow>
    </PanelSection>
  );
};

export default definePlugin(() => {
  return {
    name: "Decky Clipper",
    titleView: <div className={staticClasses.Title}>Decky Clipper</div>,
    content: <Content />,
    icon: <FaCameraRetro />,
    onDismount() {
    },
  };
});
