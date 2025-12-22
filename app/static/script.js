async function sendImage() {
    const fileInput = document.getElementById("image");
    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append("uploaded_file", file);

    const response = await fetch("/model/uploadfile/", {
        method: "POST",
        body: formData
    });

    const text = await response.text();
    document.getElementById("top").innerText = "Результат: " + text;
}

function send() {
    console.log("BUTTON CLICKED");

    const fileInput = document.getElementById("image");
    console.log(fileInput.files);
}