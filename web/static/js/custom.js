document.addEventListener('DOMContentLoaded', () => {

  // Get all "navbar-burger" elements
  const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

  // Check if there are any navbar burgers
  if ($navbarBurgers.length > 0) {

    // Add a click event on each of them
    $navbarBurgers.forEach(el => {
      el.addEventListener('click', () => {

        // Get the target from the "data-target" attribute
        const target = el.dataset.target;
        const $target = document.getElementById(target);

        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        el.classList.toggle('is-active');
        $target.classList.toggle('is-active');

      });
    });
  }
});


function IsLoading() {
  var element = document.getElementById("button");
  element.classList.toggle("is-loading");
}

function RenameElement(element, text) {
  var element = document.getElementById(element)
  element.outerText = text;
}

function HideElement(element) {
  var element = document.getElementById(element)
  element.style.display = "none";
  return true;
}

function ShowElement(element) {
  var element = document.getElementById(element)
  element.style.display = "block";
  return true;
}

function AddElementToList(tag, list) {
  var url = '/hashtag/add/' + list + '/' + tag + '/'
  var xhr = new XMLHttpRequest();
  xhr.open('GET', url, true); //url используется здесь
  xhr.send();
  if (xhr.status != 200) {
    console.log(xhr.status + ': ' + xhr.statusText);
  } else {
    console.log(xhr.responseText);
  }
}

function AddElementToBlacklist(blacklist) {
  var url = '/blacklist/add/' + blacklist + '/'
  var xhr = new XMLHttpRequest();
  xhr.open('GET', url, true);
  xhr.send();
  if (xhr.status != 200) {
    console.log(xhr.status + ': ' + xhr.statusText);
  } else {
    console.log(xhr.responseText);
  }
}


function NavbarListSelect() {
  var element = document.getElementById("NavbarListSelect");
  element.classList.toggle("is-active");
  return true;
}

function ActivateModal(name) {
  var element = document.getElementById(name);
  element.classList.toggle("is-active");
  return true;
}

function DeActivateModal(name) {
  var element = document.getElementById(name)
  element.classList.remove("is-active");
  return true;
}

function HideCommentInReport(comment_id) {
  var url = '/comment/' + comment_id + '/read'
  var xhr = new XMLHttpRequest();
  xhr.open('GET', url, true);
  xhr.send();
  if (xhr.status != 200) {
    console.log(xhr.status + ': ' + xhr.statusText);
  } else {
    console.log(xhr.responseText);
  }
}

function DeleteAccount(account_id) {
  var url = '/profiles/' + account_id + '/delete'
  var xhr = new XMLHttpRequest();
  xhr.open('GET', url, true);
  xhr.send();
  if (xhr.status != 200) {
    console.log(xhr.status + ': ' + xhr.statusText);
  } else {
    console.log(xhr.responseText);
  }
}

function ProfilesUpdate() {
  var url = '/profiles-update'
  var xhr = new XMLHttpRequest();
  xhr.open('GET', url, true);
  xhr.send();
  if (xhr.status != 200) {
    console.log(xhr.status + ': ' + xhr.statusText);
  } else {
    console.log(xhr.responseText);
  }
}

function ReloadPage() {
  document.location.reload();
}