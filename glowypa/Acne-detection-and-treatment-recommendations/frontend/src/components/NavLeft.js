import React, { useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";

import "./css/Navleft.css";

import { ReactComponent as ReportIcon } from "../assets/icons/report.svg";
import { ReactComponent as SettingIcon } from "../assets/icons/setting.svg";
import { ReactComponent as LogoutIcon } from "../assets/icons/logout.svg";
import { ReactComponent as DemoIcon } from "../assets/icons/demo.svg";
import { ReactComponent as ScanIcon } from "../assets/icons/scan.svg";
import { ReactComponent as MedicalRecordIcon } from "../assets/icons/medicalrecord.svg";

import Avatar from "../assets/avatars/avatar.jpg";
import Tooltip from "./Tooltip";
import YesNoDialog from "./YesNoDialog";

import SettingDialog from "./settingDialog";

export default function NavLeft() {
  const dispatch = useDispatch();

  // setting dialog
  const isActiveDialogSetting = useSelector(
    (state) => state.activeDialog.isActiveDialogSetting
  );

  const handleOpenSettingDialog = () => {
    dispatch({ type: "ACTIVE_DIALOG_SETTING" });
  };

  const handleCloseSettingDialog = () => {
    dispatch({ type: "CLOSE_DIALOG_SETTING" });
  };
  //
  const [openLogoutDialog, setOpenLogoutDialog] = React.useState(false);
  const [notification, setNotification] = React.useState("");
  const navigate = useNavigate();

  const location = useLocation();
  const isActivePath = (path) => location.pathname === path;

  const handleClickNav = (path) => {
    navigate(path);
  };

  const handleClickLogout = () => {
    setOpenLogoutDialog(true);
    setNotification("Do you want to logout");
  };

  const handleAccept = (value) => {
    if (value) {
      localStorage.removeItem("authToken");
      localStorage.removeItem("userData");
      window.location.href = "/";
    } else if (!value) {
      setOpenLogoutDialog(false);
    }
  };

  useEffect(() => {
    console.log(isActiveDialogSetting);
  }, [isActiveDialogSetting]);

  return (
    <>
      {openLogoutDialog ? (
        <YesNoDialog notification={notification} handleAccept={handleAccept} />
      ) : (
        ""
      )}
      {isActiveDialogSetting ? (
        <SettingDialog handleCloseSettingDialog={handleCloseSettingDialog} />
      ) : (
        ""
      )}
      <div className="nav__left box--shadow-btn">
        <div className="nav__left--avatar">
          <div className="avatar">
            <img src={Avatar} alt="Description of image" />
          </div>
        </div>
        <div className="nav__left--func">
          <div className="nav__left--head">
            <Tooltip text="Demo">
              <div
                className={`icon ${isActivePath("/demo") ? "icon-active" : ""}`}
                // onClick={() => handleClickNav("/demo")}
              >
                <DemoIcon className="icon--element" />
              </div>
            </Tooltip>
            <Tooltip text="Acne scan daily">
              <div
                className={`icon ${
                  isActivePath("/diagnosis") ? "icon-active" : ""
                }`}
                onClick={() => handleClickNav("/diagnosis")}
              >
                <ScanIcon className="icon--element" />
                <span className="span-active"></span>
              </div>
            </Tooltip>
            <Tooltip text="Skin health monitoring">
              <div
                className={`icon ${isActivePath("/test") ? "icon-active" : ""}`}
              >
                <MedicalRecordIcon className="icon--element" />
              </div>
            </Tooltip>
          </div>
          <div className="nav__left--bottom">
            <Tooltip text="Settings">
              <div className="icon" onClick={() => handleOpenSettingDialog()}>
                <SettingIcon className="icon--element" />
              </div>
            </Tooltip>
            <Tooltip text="Feedback">
              <div className="icon">
                <ReportIcon className="icon--element" />
              </div>
            </Tooltip>
            <Tooltip text="Logout">
              <div className="icon" onClick={() => handleClickLogout()}>
                <LogoutIcon className="icon--element" />
              </div>
            </Tooltip>
          </div>
        </div>
      </div>
    </>
  );
}
