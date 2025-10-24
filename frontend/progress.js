function handleForm(formId, resultId, videoType) {
    document.getElementById(formId).onsubmit = async function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const xhr = new XMLHttpRequest();
        xhr.open("POST", `/upload/${videoType}`);
        xhr.upload.onprogress = function(event) {
            if (event.lengthComputable) {
                const percent = Math.round((event.loaded / event.total) * 100);
                document.getElementById(resultId).innerHTML = `<div class='progress'><div class='progress-bar' role='progressbar' style='width:${percent}%' aria-valuenow='${percent}' aria-valuemin='0' aria-valuemax='100'>${percent}%</div></div>`;
            }
        };
        xhr.onload = function() {
            if (xhr.status === 200) {
                let resp = {};
                try {
                    resp = JSON.parse(xhr.responseText);
                } catch (e) {
                    document.getElementById(resultId).innerText = "Error: Invalid response format. " + e.message;
                    return;
                }
                let html = `<div class='fw-bold mb-2'>Count: ${resp.count ?? 'N/A'}</div>`;
                if (resp.video_url && resp.video_filename) {
                    html += `<a href='${resp.video_url}' download='${resp.video_filename}' class='btn btn-success w-100 mt-2'>Download Result Video</a>`;
                } else {
                    html += `<div class='text-danger mt-2'>Result video not available.</div>`;
                }
                document.getElementById(resultId).innerHTML = html;
            } else {
                document.getElementById(resultId).innerText = "Error: " + xhr.statusText;
            }
        };
        xhr.onerror = function() {
            document.getElementById(resultId).innerText = "Error: Network error - Make sure backend is running on port 8000";
        };
        xhr.send(formData);
    };
}
handleForm("form-market", "result-market", "market_square");
handleForm("form-grocery", "result-grocery", "grocery_store");
handleForm("form-subway", "result-subway", "subway");
