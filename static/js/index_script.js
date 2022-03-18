$(document).ready(function () {
  $("#api-form").submit(function (event) {
    event.preventDefault();

    let token = $("#api-form input")[0].value;
    $.post("/init", { api_token: token }, (data, status) => {
      // console.log(data, status);
      if (data["response"] != 200) {
        let form_error = $("#form-error");
        form_error.html(data["error_msg"]);
        form_error.css({ display: "block" });
      } else {
        window.location.href = "/data";
      }
    });
  });
});
