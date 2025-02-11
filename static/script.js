document.addEventListener("DOMContentLoaded", function() {
  // Für den Teststreamer; in der echten Anwendung wird die streamerId dynamisch gesetzt
  const streamerId = "example_streamer";

  // Affiliate-Daten für den Streamer abrufen
  fetch(`/affiliate/${streamerId}`)
    .then(response => response.json())
    .then(data => {
      // Fallback-Werte
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

      // Erstelle Carousel-Items aus den zurückgegebenen Videos
      const carouselItems = videos.map(videoSrc => ({
        videoSrc: videoSrc,
        affiliateUrl: affiliateUrl,
        streamerName: streamerName
      }));

      const carouselContainer = document.getElementById("video-carousel");

      // Für jedes Item wird ein Container mit Video und Overlay erstellt
      carouselItems.forEach((item, index) => {
        const itemDiv = document.createElement("div");
        itemDiv.classList.add("carousel-item");
        if (index === 0) itemDiv.classList.add("active");

        // Video-Element erzeugen
        const videoElem = document.createElement("video");
        videoElem.src = item.videoSrc;
        videoElem.autoplay = true;
        videoElem.loop = true;
        videoElem.muted = true;

        // Overlay mit Affiliate-Link erstellen; sichtbarer Text ist der Streamername
        const overlay = document.createElement("div");
        overlay.classList.add("affiliate-overlay");
        overlay.innerHTML = `<a href="${item.affiliateUrl}" target="_blank">${item.streamerName}</a>`;

        itemDiv.appendChild(videoElem);
        itemDiv.appendChild(overlay);
        carouselContainer.appendChild(itemDiv);
      });

      // Rotationslogik: Wechsle alle 5 Sekunden das aktive Element
      let currentIndex = 0;
      setInterval(() => {
        const items = document.querySelectorAll(".carousel-item");
        items[currentIndex].classList.remove("active");
        currentIndex = (currentIndex + 1) % items.length;
        items[currentIndex].classList.add("active");
      }, 5000);
    })
    .catch(error => {
      console.error("Error fetching affiliate data:", error);
    });
});
