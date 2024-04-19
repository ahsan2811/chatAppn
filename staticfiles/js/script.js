const userLinks = document.querySelectorAll(".user-link");
const message_container = document.querySelector(".message-container");
const text_message = document.getElementById("text-message");
const accept_requests = document.querySelectorAll(".accept-request-button");
const messageContainer = document.getElementById("message-container");
const friends_list_container = document.querySelector(
  ".friends-list-container"
);
const make_friends = document.getElementById("make-friends");
let person_id;
let chat_websocket;

//----------------------------------------------------------------
const sendToWebsocket = function () {
  const send = document.getElementById("send-button");
  send.addEventListener("click", function () {
    chat_websocket.send(
      `{"type":"new_message","message":"${text_message.value}"}`
    );
    const currentDate = new Date();

    // Get date components
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth() + 1; // Month is zero-based, so add 1
    const day = currentDate.getDate();
    const hours = currentDate.getHours();
    const minutes = currentDate.getMinutes();
    const seconds = currentDate.getSeconds();

    // Format date and time
    const formattedDateTime = `${year}-${month
      .toString()
      .padStart(2, "0")}-${day.toString().padStart(2, "0")} ${hours
      .toString()
      .padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${seconds
      .toString()
      .padStart(2, "0")}`;

    const newMessageDiv = document.createElement("div");
    newMessageDiv.classList.add(
      "from-me",
      "col-6",
      "px-2",
      "bg-primary",
      "text-white",
      "my-corners-me",
      "d-flex",
      "justify-content-between",
      "align-items-center"
    );
    newMessageDiv.innerHTML = `
      <p class="fw-semibold" style="width: 50%">
        ${text_message.value}
      </p>
      <div class="mb-auto mt-1 d-flex hstack gap-1">
        <div class="status rounded-circle-bg-primary"></div>
        <div class="status rounded-circle-bg-primary"></div>
        <div class="status rounded-circle-bg-primary"></div>
      </div>
      <p class="small mb-auto">${formattedDateTime}</p>
    `;
    message_container.prepend(newMessageDiv);
    text_message.value = "";
  });
};

const connectToWebsocket = function (person_id) {
  const url = `ws://127.0.0.1:8000/websocket/${person_id}/`;
  chat_websocket = new WebSocket(url);
  chat_websocket.onopen = function () {
    chat_websocket.send(`{"type":"entered_chat"}`);
  };
  chat_websocket.onmessage = function (event) {
    const received_data = JSON.parse(event.data);
    if (received_data.type_of_data == "new_message") {
      const newMessageDiv = document.createElement("div");
      newMessageDiv.classList.add(
        "to-me",
        "col-6",
        "offset-6",
        "px-2",
        "bg-dark",
        "text-white",
        "my-corners-to",
        "d-flex",
        "justify-content-between",
        "align-items-center"
      );
      newMessageDiv.innerHTML = `
        <p class="fw-semibold" style="width: 50%">
          ${received_data.data}
        </p>
        
        <p class="small mb-auto">Date: 2024, 02, 11:45</p>
      `;
      message_container.prepend(newMessageDiv);
      chat_websocket.send(`{"type":"message_seen"}`);
    } else if (received_data.type_of_data == "message_seen") {
      const message_seen = document.getElementsByClassName("status");

      for (let i = 0; i < message_seen.length; i++) {
        message_seen[i].classList.remove("rounded-circle-bg-primary");
        message_seen[i].classList.add("rounded-circle-bg-seen");
      }
    }
  };
};

//---------------------------------------------------------------
for (let index = 0; index < userLinks.length; index++) {
  const link = userLinks[index];

  link.addEventListener("click", function (e) {
    message_container.innerHTML = ``;

    const string = link.dataset.url;
    person_id = parseInt(string.match(/\d+/)[0], 10);

    fetch(link.dataset.url)
      .then((response) => response.json())
      .then((response) => {
        const userlist = JSON.parse(response.user);
        const user_id = userlist[0].pk;

        const mymessages = JSON.parse(response.messages);
        const userNameDiv = document.createElement("div");
        userNameDiv.innerHTML = `<h4>${response.person_first_name} ${response.person_last_name}</h4>`;
        message_container.prepend(userNameDiv);
        mymessages.forEach((m) => {
          const newMessageDiv = document.createElement("div");

          if (user_id == m.fields.sender) {
            person_id = m.fields.receiver;

            newMessageDiv.classList.add(
              "from-me",
              "col-6",
              "px-2",
              "bg-primary",
              "text-white",
              "my-corners-me",
              "d-flex",
              "justify-content-between",
              "align-items-center"
            );
            newMessageDiv.innerHTML = `<p class="fw-semibold" style="width: 50%">
            ${m.fields.message}
            
          </p>
          <div class="mb-auto mt-1 d-flex hstack gap-1">
          ${
            m.fields.seen
              ? `<div class="status rounded-circle-bg-seen"></div>
             <div class="status rounded-circle-bg-seen"></div>
             <div class="status rounded-circle-bg-seen"></div>`
              : `<div class="status rounded-circle-bg-primary"></div>
              <div class="status rounded-circle-bg-primary"></div>
              <div class="status rounded-circle-bg-primary"></div>`
          }
          </div>
        
          <p class="small mb-auto">${m.fields.date} ${m.fields.time}`;
            message_container.prepend(newMessageDiv);
          } else {
            person_id = m.fields.sender;

            newMessageDiv.classList.add(
              "to-me",
              "col-6",
              "offset-6",
              "px-2",
              "bg-dark",
              "text-white",
              "my-corners-to",
              "d-flex",
              "justify-content-between",
              "align-items-center"
            );
            newMessageDiv.innerHTML = `<p class="fw-semibold" style="width: 50%">
            ${m.fields.message}
          </p>
        
          <p class="small mb-auto">${m.fields.date} ${m.fields.time}`;
            message_container.prepend(newMessageDiv);
          }
        });
        console.log("aloo");
        connectToWebsocket(person_id);
      });
  });
}
sendToWebsocket();
