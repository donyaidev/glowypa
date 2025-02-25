import "./css/settingDialog.css";
import React, { useState } from "react";
import { ReactComponent as MultipleImg } from "../assets/icons/multiple.svg";
import { useSelector } from "react-redux";
import Avatar from "../assets/avatars/avatar.jpg";

const SettingDialog = ({ handleCloseSettingDialog }) => {
  const [formDataInformation, setFormDataInformation] = useState({
    first_name: useSelector((state) => state.user.user.first_name),
    last_name: useSelector((state) => state.user.user.last_name),
    birth_date: useSelector((state) => state.user.user.birth_date),
    gender: "",
    skin_type: useSelector((state) => state.user.user.skin_type),
    location: useSelector((state) => state.user.user.location),
  });

  const [formAccount, setFormAccount] = useState({
    email: useSelector((state) => state.user.user.email),
    password_old: "",
    password_new: "",

  });

  const [isEditingInformation, setIsEditingInformation] = useState(false);
  const [isEditingAccount, setIsEditingAccount] = useState(false);

  const handleChangeSecure = (event) => {
    const { name, value } = event.target;
    setFormAccount({
      ...formAccount,
      [name]: value,
    });
    console.log(formAccount);
  };

  const handleChangeInformation = (event) => {
    const { name, value } = event.target;
    setFormDataInformation({
      ...formDataInformation,
      [name]: value,
    });
    console.log(name);
  };

  const handleInformationSubmit = (event) => {
    event.preventDefault();
    console.log("Form thông tin đã được gửi:", formDataInformation);
    setIsEditingInformation(false); 
  };

  const handleAccountSubmit = (event) => {
    event.preventDefault();
    console.log("Form tài khoản đã được gửi:", formAccount);
    setIsEditingAccount(false); 
  };

  const toggleInformationEditMode = () => {
    if (isEditingInformation) {
      handleInformationSubmit(new Event("submit"));
    } else {
      setIsEditingInformation(true);
    }
  };

  const toggleAccountEditMode = () => {
    if (isEditingAccount) {
      handleAccountSubmit(new Event("submit"));
    } else {
      setIsEditingAccount(true);
    }
  };

  return (
    <div className="setting__background">
      <div className="setting__background--frame box--shadow-btn">
        <div className="setting__header">
          <p className="font-header">Cài đặt</p>
          <div
            className="setting__close"
            onClick={() => handleCloseSettingDialog()}
          >
            <MultipleImg className="icon--element-mul" />
          </div>
        </div>
        <div className="setting__content">
          <div className="setting__content--left">
            <div className="setting__content--avt">
              <div className="avatar">
                <img src={Avatar} alt="Description of image" />
              </div>
            </div>
          </div>
          <div className="setting__content--right">
            <form className="form__grid" onSubmit={handleInformationSubmit}>
              <div className="item__first-name">
                <label>Tên</label>
                <input
                  type="text"
                  name="first_name"
                  value={formDataInformation.first_name}
                  onChange={handleChangeInformation}
                  disabled={!isEditingInformation}
                  className={!isEditingInformation ? "dont__fillin" : ""}
                />
              </div>
              <div className="item__last-name">
                <label>Họ</label>
                <input
                  type="text"
                  name="last_name"
                  value={formDataInformation.last_name}
                  onChange={handleChangeInformation}
                  disabled={!isEditingInformation}
                  className={!isEditingInformation ? "dont__fillin" : ""}
                />
              </div>

              <div className="item__birth-day">
                <label>Ngày sinh</label>
                <input
                  type="date"
                  name="birth_date"
                  value={formDataInformation.birth_date}
                  onChange={handleChangeInformation}
                  disabled={!isEditingInformation}
                  className={!isEditingInformation ? "dont__fillin" : ""}
                />
              </div>
              <div className="item__skin-type">
                <label className="">Loại da</label>
                <select
                  name="skin_type"
                  value={formDataInformation.skin_type}
                  onChange={handleChangeInformation}
                  disabled={!isEditingInformation}
                  className={!isEditingInformation ? "dont__fillin" : ""}
                  required
                >
                  <option value="">Chọn loại da của bạn</option>
                  <option value="normal">Bình thường</option>
                  <option value="oily">Dầu</option>
                  <option value="dry">Khô</option>
                  <option value="combination">Hỗn hợp</option>
                  <option value="sensitive">Nhạy cảm</option>
                  <option value="acne-prone">Dễ bị mụn</option>
                </select>
              </div>
              <div className="item__address">
                <label className="">Địa chỉ</label>
                <input
                  type="text"
                  name="location"
                  placeholder="Thành phố, Quốc gia của bạn"
                  value={formDataInformation.location}
                  onChange={handleChangeInformation}
                  disabled={!isEditingInformation}
                  className={!isEditingInformation ? "dont__fillin" : ""}
                  required
                />
              </div>
              <div className="edit__information item__btn">
                <button
                  type="button"
                  className={`edit--btn ${
                    isEditingInformation ? "btn-save" : "btn-edit"
                  }`}
                  onClick={toggleInformationEditMode}
                >
                  {isEditingInformation ? "Lưu" : "Chỉnh sửa"}
                </button>
              </div>
            </form>

            <form onSubmit={handleAccountSubmit}>
              <div className="grid__secure">
                <div className="grid__secure--item">
                  <label className="">Email</label>
                  <input
                    type="email"
                    name="email"
                    placeholder="Địa chỉ Email"
                    value={formAccount.email}
                    onChange={handleChangeSecure}
                    disabled={!isEditingAccount}
                    className={!isEditingAccount ? "dont__fillin" : ""}
                    required
                  />
                </div>
                <div className="grid__secure--item">
                  <label className="">Mật khẩu cũ</label>
                  <input
                    type="password"
                    name="password_old"
                    placeholder="Mật khẩu cũ"
                    value={formAccount.password}
                    onChange={handleChangeSecure}
                    disabled={!isEditingAccount}
                    className={!isEditingAccount ? "dont__fillin" : ""}
                    minLength={8}
                    required
                  />
                </div>
                <div className="grid__secure--item">
                  <label className="">Mật khẩu mới</label>
                  <input
                    type="password"
                    name="password_new"
                    placeholder="Mật khẩu mới"
                    value={formAccount.password}
                    onChange={handleChangeSecure}
                    disabled={!isEditingAccount}
                    className={!isEditingAccount ? "dont__fillin" : ""}
                    minLength={8}
                    required
                  />
                </div>
              </div>
              <div className="edit__information">
                <button
                  type="button"
                  className={`edit--btn ${
                    isEditingAccount ? "btn-save" : "btn-edit"
                  }`}
                  onClick={toggleAccountEditMode}
                >
                  {isEditingAccount ? "Lưu" : "Đổi mật khẩu"}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingDialog;
