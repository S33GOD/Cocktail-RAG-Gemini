async function sendMessage() {
            try{
                document.getElementById("loadingIndicator").style.display = "block";
                let userInput = document.getElementById("userInput").value;

                let response = await fetch("http://127.0.0.1:8000/chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ user_input: userInput })
                })
                .catch(error => {
                    // Handle any error
                    console.error("Error:", error);
                });

                let data = await response.json();
                console.log(data.response.response)
                document.getElementById("output").innerHTML = data.response.response;
                document.getElementById("loadingIndicator").style.display = "none";
                document.getElementById("output").innerHTML = data.response.response;
            } catch (error) {
                document.getElementById("loadingIndicator").style.display = "none";
                document.getElementById("output").innerHTML = "Error: Unable to fetch data.";
                console.error(error);
            }
}

