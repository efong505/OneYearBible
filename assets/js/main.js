let date = new Date();
let year = date.getFullYear();
let month = date.getMonth();

const day = document.querySelector(".calendar-dates");
const currdate = document.querySelector(".calendar-current-date");
const prenexIcons = document.querySelectorAll(".calendar-navigation span");

const months = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

let clickedDay = null;
let selectedDayElement = null;

const manipulate = () => {
  let dayone = new Date(year, month, 1).getDay();
  let lastdate = new Date(year, month + 1, 0).getDate();
  let dayend = new Date(year, month, lastdate).getDay();
  let monthlastdate = new Date(year, month, 0).getDate();

  let lit = "";

  for (let i = dayone; i > 0; i--) {
    lit += `<li class="inactive">${monthlastdate - i + 1}</li>`;
  }

  
  for (let i = 1; i <= lastdate; i++) {
    let isToday = (i === date.getDate()
      && month === new Date().getMonth()
      && year === new Date().getFullYear()) ? "active" : "";

    let highlightClass = (clickedDay === i) ? "highlight" : "";

    lit += `<li class="${isToday} ${highlightClass}" data-day="${i}">${i}</li>`;
  }


  for (let i = dayend; i < 6; i++) {
    lit += `<li class="inactive">${i - dayend + 1}</li>`;
  }

  currdate.innerText = `${months[month]} ${year}`;
  day.innerHTML = lit;

  addClickListenersToDays();
};


function addClickListenersToDays() {
  const allDays = day.querySelectorAll('li:not(.inactive)');
  allDays.forEach(li => {
    li.addEventListener('click', () => {
      if (selectedDayElement) {
        selectedDayElement.classList.remove('highlight');
      }

      li.classList.add('highlight');
      selectedDayElement = li;

      clickedDay = parseInt(li.getAttribute('data-day'));
      
      // Navigate to Bible reading for selected date
      navigateToBibleReading(year, month, clickedDay);
    });
  });
}

function navigateToBibleReading(year, month, day) {
  // Check if this is September 22
  if (month === 8 && day === 22) { // month is 0-indexed, so 8 = September
    window.location.href = 'other/0922.html';
    return;
  }
  
  // Calculate day of year for other dates
  const selectedDate = new Date(year, month, day);
  const startOfYear = new Date(year, 0, 1);
  const dayOfYear = Math.floor((selectedDate - startOfYear) / (24 * 60 * 60 * 1000)) + 1;
  
  // For real implementation, use consistent naming like:
  const readingUrl = `day${dayOfYear.toString().padStart(3, '0')}.html`;
  console.log(`Navigate to ${readingUrl}`);
  // window.location.href = readingUrl;
}

function goToToday() {
  const today = new Date();
  year = today.getFullYear();
  month = today.getMonth();
  
  // Clear previous selection
  clickedDay = null;
  selectedDayElement = null;
  
  // Refresh calendar
  manipulate();
  
  // Navigate to today's reading
  navigateToBibleReading(year, month, today.getDate());
}

manipulate();

prenexIcons.forEach(icon => {
  icon.addEventListener("click", () => {
    month = icon.id === "calendar-prev" ? month - 1 : month + 1;

    if (month < 0 || month > 11) {
      date = new Date(year, month, new Date().getDate());
      year = date.getFullYear();
      month = date.getMonth();
    } else {
      date = new Date();
    }

    clickedDay = null;
    selectedDayElement = null;

    manipulate();
  });
});

// Add event listener for Today button
document.getElementById('today-btn').addEventListener('click', goToToday);