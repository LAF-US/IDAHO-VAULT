<%*
// ROYGBIV weekday color sync — Templater startup template
// Applies body class so roygbiv-smtwtfs.css can set the vault accent color
const dayMap = {
  0: "roygbiv-sun", 1: "roygbiv-mon", 2: "roygbiv-tue",
  3: "roygbiv-wed", 4: "roygbiv-thu", 5: "roygbiv-fri",
  6: "roygbiv-sat"
};
const today = new Date().getDay();
document.body.className = document.body.className.replace(/roygbiv-\w+/g, "").trim();
document.body.classList.add(dayMap[today]);
%>
