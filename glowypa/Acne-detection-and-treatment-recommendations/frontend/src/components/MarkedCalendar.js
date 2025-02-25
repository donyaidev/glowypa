import React, { useState } from 'react';
import { ReactComponent as ArrowLeft } from '../assets/icons/arrow-left.svg';
import { ReactComponent as ArrowRight } from '../assets/icons/arrow-right.svg';

  const MarkedCalendar = () => {
    const [currentDate, setCurrentDate] = useState(new Date(2024, 8)); // Tháng 9 năm 2024
    const markedDates = [10, 15, 30]; // Ngày được đánh dấu

    const daysOfWeek = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'];

    const getDaysInMonth = (date) => {
      const year = date.getFullYear();
      const month = date.getMonth();
      return new Date(year, month + 1, 0).getDate();
    };

    const handlePrevMonth = () => {
      setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1));
    };

    const handleNextMonth = () => {
      setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1));
    };

    const renderDays = () => {
      const daysInMonth = getDaysInMonth(currentDate);
      const firstDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1).getDay();
      const days = [];

      // Fill in the blanks for the first row
      for (let i = 0; i < firstDayOfMonth; i++) {
        days.push(<div key={`blank-${i}`} className="day blank"></div>);
      }

      // Add the days of the month
      for (let day = 1; day <= daysInMonth; day++) {
        const isMarked = markedDates.includes(day);
        days.push(
          <div key={day} className={`day${isMarked ? ' marked' : ''}`}>
            {day}
          </div>
        );
      }

      return days;
    };

    return (
      <div className="calendar  box--shadow-btn">
        <div className="header">
          <button className='calendar-btn  box--shadow-btn' onClick={handlePrevMonth}>
            <ArrowLeft className="calendar-icon"/>
          </button>
          <span className='month-year'>
            {currentDate.toLocaleString('default', { month: 'short' })} {currentDate.getFullYear()}
          </span>
          <button className='calendar-btn  box--shadow-btn' onClick={handleNextMonth}>
            <ArrowRight className="calendar-icon"/>
          </button>
          <button className="today-button box--shadow-btn">Today</button>
        </div>
        <div className="days-of-week">
          {daysOfWeek.map((day, index) => (
            <div key={index} className="day-name">{day}</div>
          ))}
        </div>
        <div className="days">{renderDays()}</div>
      </div>
    );
  };

  export default MarkedCalendar;