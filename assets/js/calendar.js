// Extract date from URL if on a reading page
let currentPageDate = null;
if (window.location.pathname.includes('/readings/')) {
  const pathParts = window.location.pathname.split('/');
  const filename = pathParts[pathParts.length - 1];
  const dateCode = filename.replace('.html', '');
  if (dateCode.match(/^\d{4}$/)) {
    const month = parseInt(dateCode.substring(0, 2)) - 1; // Convert to 0-based month
    const day = parseInt(dateCode.substring(2, 4));
    currentPageDate = { month, day };
    console.log('Extracted date from URL:', { dateCode, month: month + 1, day, currentPageDate });
  }
}

let widgetYear = 2025; // Set to 2025 for the Bible reading plan
let widgetMonth = currentPageDate ? currentPageDate.month : new Date().getMonth();

const widgetDates = document.querySelector(".widget-dates");
const widgetCurrentDate = document.querySelector(".widget-current-date");
const widgetNavIcons = document.querySelectorAll(".widget-navigation span");
const todayBtn = document.getElementById('today-btn');

const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const monthNames = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"];

// Load available readings from reading plan
let availableReadings = [];

// Load reading plan to get available dates
const basePath = window.location.pathname.includes('/readings/') ? '../../assets/data/' : 'assets/data/';
fetch(`${basePath}reading-plan.json`)
  .then(response => response.json())
  .then(data => {
    availableReadings = Object.keys(data);
    window.availableReadings = availableReadings;
    console.log('Loaded readings:', availableReadings.length);
    renderWidget();
  })
  .catch(error => {
    console.error('Error loading reading plan:', error);
    availableReadings = [];
    renderWidget();
  });

const renderWidget = () => {
  let firstDay = new Date(widgetYear, widgetMonth, 1).getDay();
  let lastDate = new Date(widgetYear, widgetMonth + 1, 0).getDate();
  let lastDay = new Date(widgetYear, widgetMonth, lastDate).getDay();
  let prevLastDate = new Date(widgetYear, widgetMonth, 0).getDate();

  let html = "";

  for (let i = firstDay; i > 0; i--) {
    html += `<li class="inactive">${prevLastDate - i + 1}</li>`;
  }

  for (let i = 1; i <= lastDate; i++) {
    const today = new Date();
    let isToday = (i === today.getDate() && widgetMonth === today.getMonth() && widgetYear === today.getFullYear()) ? "active" : "";
    let isCurrentPage = (currentPageDate && i === currentPageDate.day && widgetMonth === currentPageDate.month) ? "current-page" : "";
    let classes = [isToday, isCurrentPage].filter(c => c).join(' ');
    
    html += `<li class="${classes}" data-day="${i}">${i}</li>`;
  }

  for (let i = lastDay; i < 6; i++) {
    html += `<li class="inactive">${i - lastDay + 1}</li>`;
  }

  widgetCurrentDate.innerText = `${months[widgetMonth]} ${widgetYear}`;
  widgetDates.innerHTML = html;

  addWidgetClickListeners();
};

function addWidgetClickListeners() {
  const allDays = widgetDates.querySelectorAll('li:not(.inactive)');
  allDays.forEach(li => {
    li.addEventListener('click', () => {
      const day = parseInt(li.getAttribute('data-day'));
      navigateToReading(widgetYear, widgetMonth, day);
    });
  });
}

function navigateToReading(year, month, day) {
  const monthStr = (month + 1).toString().padStart(2, '0');
  const dayStr = day.toString().padStart(2, '0');
  const dateCode = monthStr + dayStr;
  
  console.log('Navigating to:', dateCode, 'Available:', availableReadings.includes(dateCode));
  
  // Check if reading exists
  if (availableReadings.includes(dateCode)) {
    if (window.location.pathname.includes('/readings/')) {
      window.location.href = `../../readings/${monthNames[month]}/${dateCode}.html`;
    } else {
      window.location.href = `readings/${monthNames[month]}/${dateCode}.html`;
    }
  } else {
    // Go to coming soon page
    if (window.location.pathname.includes('/readings/')) {
      window.location.href = `../../coming-soon.html?date=${year}-${monthStr}-${dayStr}`;
    } else {
      window.location.href = `coming-soon.html?date=${year}-${monthStr}-${dayStr}`;
    }
  }
}

function goToToday() {
  const today = new Date();
  navigateToReading(today.getFullYear(), today.getMonth(), today.getDate());
}

// Initial render happens after loading reading plan

widgetNavIcons.forEach(icon => {
  icon.addEventListener("click", () => {
    widgetMonth = icon.id === "widget-prev" ? widgetMonth - 1 : widgetMonth + 1;

    if (widgetMonth < 0) {
      widgetMonth = 11;
      widgetYear--;
    } else if (widgetMonth > 11) {
      widgetMonth = 0;
      widgetYear++;
    }

    renderWidget();
  });
});

if (todayBtn) {
  todayBtn.addEventListener('click', goToToday);
}