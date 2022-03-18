Chart.defaults.global.defaultFontColor = "white";

$(document).ready(function () {
  // Load the group picker
  $("#groups-loading").css({ display: "block" });
  $("#group-select").css({ display: "none" });

  $.get("/groups", (data, status) => {
    let group_select_inner = "";
    for (let i = 0; i < data.length; i++) {
      group_select_inner +=
        '<option value="' + data[i].id + '">' + data[i].name + "</option>";
    }
    $("#group-select").html(group_select_inner);
    $("#groups-loading").css({ display: "none" });
    $("#group-select").css({ display: "block" });
  });

  var ctx = document.getElementById("talksMostCanvas").getContext("2d");
  var talksMostChart = new Chart(ctx, {
    // The type of chart we want to create
    type: "bar",

    // The data for our dataset
    data: {
      // labels: data["labels"],
      datasets: [
        {
          label: "Top Message Senders",
          backgroundColor: "rgb(245, 129, 66)",
          // data: data["data"],
        },
      ],
    },

    // Configuration options go here
    options: {
      legend: {
        labels: {
          // This more specific font property overrides the global property
          fontColor: "white",
        },
      },
      scales: {
        xAxes: [
          {
            gridLines: {
              color: "white",
            },
          },
        ],
      },
    },
  });

  var ctx = document.getElementById("likesPerMessageCanvas").getContext("2d");
  var likesPerMessageChart = new Chart(ctx, {
    // The type of chart we want to create
    type: "bar",

    // The data for our dataset
    data: {
      // labels: data["labels"],
      datasets: [
        {
          label: "Likes Per Message Ratio",
          backgroundColor: "rgb(255, 99, 132)",
          borderColor: "rgb(255, 99, 132)",
          // data: data["data"],
        },
      ],
    },

    // Configuration options go here
    options: {},
  });

  $("#group-select-btn").click(() => {
    let group_id = $("#group-select").val();
    let reload_messages = $("#reload-data-checkbox").prop("checked");

    $("#total-messages-count-loading").css({ display: "block" });
    $("#total-messages").css({ display: "none" });

    $.get(
      "/countMessages",
      { group_id: group_id, reload_messages: reload_messages },
      (data, status) => {
        $("#total-messages").html(data);
        $("#total-messages").css({ display: "block" });
        $("#total-messages-count-loading").css({ display: "none" });
      }
    );

    $(".group-info-loading").css({ display: "block" });
    $("#total-members").css({ display: "none" });
    $("#date-created").css({ display: "none" });

    $.get("/groupInfo", { group_id: group_id }, (data, status) => {
      $("#total-members").html(data["num_members"]);
      $("#date-created").html(data["created_on"]);
      $(".group-info-loading").css({ display: "none" });
      $("#total-members").css({ display: "block" });
      $("#date-created").css({ display: "block" });
    });

    $.get(
      "/messagesPerPerson",
      {
        group_id: group_id,
        reload_messages: reload_messages,
      },
      (data, status) => {
        talksMostChart.data.labels = data["labels"];
        talksMostChart.data.datasets[0].data = data["data"];
        talksMostChart.update();
      }
    );

    $.get(
      "/likesPerMessage",
      {
        group_id: group_id,
        reload_messages: reload_messages,
      },
      (data, status) => {
        likesPerMessageChart.data.labels = data["labels"];
        likesPerMessageChart.data.datasets[0].data = data["data"];
        likesPerMessageChart.update();
      }
    );
  });
});
