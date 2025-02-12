document.addEventListener("DOMContentLoaded", function() {
  // Für Testzwecke: Verwende hier die korrekte Twitch User ID, die vom OAuth-Flow validiert wird.
  const streamerId = "1078778564";

  // Platzhalter für einen echten Access Token und die Client-ID; in der Produktion werden diese dynamisch gesetzt.
  const accessToken = "jk4f3luwq1oroz2mdyhdfmdxnjaly8";
  const clientId = "gp762nuuoqcoxypju8c569th9wz7q5";

  function loadAffiliateData() {
    fetch(`/affiliate/${streamerId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Client-ID': clientId
      }
    })
    .then(response => {
      if (response.status === 200) {
        return response.json();
      } else if (response.status === 404) {
        return null;
      } else {
        throw new Error('Error loading affiliate data');
      }
    })
    .then(data => {
      if (data) {
        document.getElementById("affiliateUrl").value = data.affiliate_url || "";
        document.getElementById("streamerName").value = data.streamer_name || "";
        if (data.videos && Array.isArray(data.videos)) {
          document.getElementById("videos").value = data.videos.join(", ");
        }
      } else {
        console.log("No affiliate data found; ready to create new entry.");
      }
    })
    .catch(error => {
      console.error("Error fetching affiliate data:", error);
    });
  }

  loadAffiliateData();

  document.getElementById("adminForm").addEventListener("submit", function(e) {
    e.preventDefault();
    const affiliateUrl = document.getElementById("affiliateUrl").value;
    const streamerName = document.getElementById("streamerName").value;
    const videosStr = document.getElementById("videos").value;
    const videos = videosStr.split(",").map(v => v.trim()).filter(v => v.length > 0);

    const payload = {
      streamer_id: streamerId,
      affiliate_url: affiliateUrl,
      streamer_name: streamerName,
      videos: videos
    };

    fetch(`/affiliate/${streamerId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
        'Client-ID': clientId
      },
      body: JSON.stringify(payload)
    })
    .then(response => response.json().then(data => ({ status: response.status, data })))
    .then(result => {
      const msgDiv = document.getElementById("adminMessage");
      if (result.status === 200) {
        msgDiv.textContent = "Settings updated successfully.";
      } else {
        msgDiv.textContent = "Error updating settings: " + result.data.message;
      }
    })
    .catch(error => {
      console.error("Error updating affiliate data:", error);
    });
  });
});
