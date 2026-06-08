fetch('/api/auth/login')

async function uploadFile() {

    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://localhost:8000/storage/upload/", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    document.getElementById("uploadResult").innerText =
        "File uploaded: " + data.url;
}