document.addEventListener("DOMContentLoaded", function() {
  // Verwende Twitch.ext.onAuthorized, um dynamisch den Access Token und die Channel ID zu erhalten
  Twitch.ext.onAuthorized(function(auth) {
    // auth.channelId ist die Twitch User ID des aktuellen Kanals
    const streamerId = auth.channelId;
    const accessToken = auth.token;
    const clientId = "gp762nuuoqcoxypju8c569th9wz7q5";

    fetch(`/affiliate/${streamerId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Client-ID': clientId
      }
    })
    .then(response => response.json())
    .then(data => {
      let affiliateUrl = "#";
      let streamerName = streamerId;
      let videos = [];

      if (data.affiliate_url) {
        affiliateUrl = data.affiliate_url;
      }
      if (data.streamer_name) {
        streamerName = data.streamer_name;
      }
      if (data.videos && Array.isArray(data.videos)) {
        videos = data.videos;
      }

      const carouselItems = videos.map(videoSrc => ({
        videoSrc: videoSrc,
        affiliateUrl: affiliateUrl,
        streamerName: streamerName
      }));

      const carouselContainer = document.getElementById("video-carousel");
      if (!carouselContainer) {
        console.error("Carousel container (#video-carousel) not found in the DOM.");
        return;
      }

      carouselItems.forEach((item, index) => {
        const itemDiv = document.createElement("div");
        itemDiv.classList.add("carousel-item");
        if (index === 0) itemDiv.classList.add("active");

        const videoElem = document.createElement("video");
        videoElem.src = item.videoSrc;
        videoElem.autoplay = true;
        videoElem.loop = true;
        videoElem.muted = true;

        const overlay = document.createElement("div");
        overlay.classList.add("affiliate-overlay");
        overlay.innerHTML = `<a href="${item.affiliateUrl}" target="_blank">${item.streamerName}</a>`;

        itemDiv.appendChild(videoElem);
        itemDiv.appendChild(overlay);
        carouselContainer.appendChild(itemDiv);
      });

      const items = document.querySelectorAll(".carousel-item");
      if (items.length > 0) {
        let currentIndex = 0;
        setInterval(() => {
          if (items.length === 0) return;
          items[currentIndex].classList.remove("active");
          currentIndex = (currentIndex + 1) % items.length;
          items[currentIndex].classList.add("active");
        }, 5000);
      } else {
        console.error("No carousel items created. Check the affiliate data and fallback values.");
      }
    })
    .catch(error => {
      console.error("Error fetching affiliate data:", error);
    });
  });
});
