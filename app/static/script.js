// async function sendImage() {
//     const fileInput = document.getElementById("image");
//     const file = fileInput.files[0];

//     const formData = new FormData();
//     formData.append("uploaded_file", file);

//     const response = await fetch("/model/uploadfile/", {
//         method: "POST",
//         body: formData
//     });

//     const text = await response.text();
//     document.getElementById("top").innerText = text;
// }

document.getElementById("button").onclick = async () => {
    const fileInput = document.getElementById("image");
    if (!fileInput.files.length) {
        alert("Choose a file!");
        return;
    }

    const loader = document.getElementById("loader");
    const resultDiv = document.getElementById("top");

    loader.style.display = "block";
    resultDiv.innerText = "";

    const formData = new FormData();
    formData.append("uploaded_file", fileInput.files[0]);

    try {
        const response = await fetch("/model/uploadfile/", {
            method: "POST",
            body: formData
        });

        const text = await response.text(); 
        resultDiv.innerText = text; 

    } catch (err) {
        console.error(err);
        resultDiv.innerText = "error";
    } finally {
        loader.style.display = "none";
    }
};
