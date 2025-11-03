// Navigation.js - Only handle Previous/Next day navigation

// Add Previous/Next day navigation (outside widget conditional)
const prevDayBtn = document.getElementById('prev-day');
const nextDayBtn = document.getElementById('next-day');

if (prevDayBtn && nextDayBtn) {
  function getCurrentPageDate() {
    const urlParams = new URLSearchParams(window.location.search);
    const currentYear = parseInt(urlParams.get('year')) || new Date().getFullYear();
    
    const pathParts = window.location.pathname.split('/');
    const filename = pathParts[pathParts.length - 1];
    const dateMatch = filename.match(/(\d{2})(\d{2})\.html/);
    
    if (dateMatch) {
      return {
        year: currentYear,
        month: parseInt(dateMatch[1]) - 1,
        day: parseInt(dateMatch[2])
      };
    }
    return { year: new Date().getFullYear(), month: 8, day: 22 };
  }
  
  prevDayBtn.addEventListener('click', (e) => {
    e.preventDefault();
    const current = getCurrentPageDate();
    const prevDate = getPreviousDay(current.year, current.month, current.day);
    navigateToDate(prevDate.year, prevDate.month, prevDate.day);
  });
  
  nextDayBtn.addEventListener('click', (e) => {
    e.preventDefault();
    const current = getCurrentPageDate();
    const nextDate = getNextDay(current.year, current.month, current.day);
    navigateToDate(nextDate.year, nextDate.month, nextDate.day);
  });
}

function getPreviousDay(year, month, day) {
  const date = new Date(year, month, day);
  date.setDate(date.getDate() - 1);
  return {
    year: date.getFullYear(),
    month: date.getMonth(),
    day: date.getDate()
  };
}

function getNextDay(year, month, day) {
  const date = new Date(year, month, day);
  date.setDate(date.getDate() + 1);
  return {
    year: date.getFullYear(),
    month: date.getMonth(),
    day: date.getDate()
  };
}

function navigateToDate(year, month, day) {
  const monthStr = (month + 1).toString().padStart(2, '0');
  const dayStr = day.toString().padStart(2, '0');
  const dateCode = monthStr + dayStr;
  
  const monthNames = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"];
  
  const yearParam = year !== new Date().getFullYear() ? `?year=${year}` : '';
  
  console.log('Navigating to:', dateCode, monthNames[month]);
  window.location.href = `../../readings/${monthNames[month]}/${dateCode}.html${yearParam}`;
}