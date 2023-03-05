function formatLogs(error) {
  let result = [];
  error.responseJSON.forEach((item, idx) => {
    if (item[2] == "Sin" || item[2] == "Cos" || item[2] == "%") {
      result.push(`<p> ${idx + 1}. timestamp: ${item[0]} , input: ${item[2]} ${
        item[1]
      } 
    output: ${item[3]}, IP: ${item[4]} </p>`);
    } else {
      result.push(`<p> ${idx + 1}. timestamp: ${item[0]} , input: ${item[1]} ${
        item[2]
      } ${item[3]}
    output: ${item[4]}, IP: ${item[5]} </p>`);
    }
  });
  result.push("<p>User operations locked for one minute</p>");
  return result;
}

function serverCall(server_data) {
  $.ajax({
    type: "POST",
    url: "/calculate",
    data: JSON.stringify(server_data),
    contentType: "application/json",
    dataType: "json",
    success: function (result) {
      document.getElementById("display").value = result;
    },
    error: function (error) {
      const errorHTML = formatLogs(error);
      document.getElementById("logs").innerHTML = errorHTML;
    },
  });
}

function calculate() {
  const displayData = document.getElementById("display").value;
  let server_data;
  if (displayData.includes("Sin")) {
    const token = displayData.split("Sin");
    server_data = { operator: "Sin", num: token[1] };
  } else if (displayData.includes("Cos")) {
    const token = displayData.split("Cos");
    server_data = { operator: "Cos", num: token[1] };
  } else if (displayData.includes("%")) {
    const token = displayData.split("%");
    server_data = { operator: "%", num: token[0] };
  } else {
    const breakdown = /([+-\/*^])/;
    const tokens = displayData.split(breakdown);
    server_data = { num: tokens[0], operator: tokens[1], num2: tokens[2] };
  }

  serverCall(server_data);
}
