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
import { useState } from "react";
import { FaCameraRetro } from "react-icons/fa";

const startRecord = callable("start_record");

function Content() {
  const [isRecording, setIsRecording] = useState(false);

  const onClick = async () => {
    startRecord();
    setIsRecording(!isRecording);
  };

  return (
    <PanelSection title="Panel Section">
      <PanelSectionRow>
        <ButtonItem
          layout="below"
          onClick={onClick}
        >
          {isRecording ? "Recording" : "Start recording"}
        </ButtonItem>
      </PanelSectionRow>
    </PanelSection>
  );
};

export default definePlugin(() => {
  console.log("Template plugin initializing, this is called once on frontend startup")

  return {
    // The name shown in various decky menus
    name: "Decky Clipper",
    // The element displayed at the top of your plugin's menu
    titleView: <div className={staticClasses.Title}>Decky Clipper</div>,
    // The content of your plugin's menu
    content: <Content />,
    // The icon displayed in the plugin list
    icon: <FaCameraRetro />,
    // The function triggered when your plugin unloads
    onDismount() {
    },
  };
});
