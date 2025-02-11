document.addEventListener("DOMContentLoaded", function() {
  // Für den Teststreamer; in der echten Anwendung wird die streamerId dynamisch gesetzt.
  const streamerId = "example_streamer";

  fetch(`/affiliate/${streamerId}`)
    .then(response => response.json())
    .then(data => {
      let affiliateUrl = "#";
      let streamerName = streamerId;
      let videos = [];

      // Falls im Response eine Fehlermeldung steht, benutze Fallback-Daten
      if (data.message && data.message === "Affiliate data not found") {
        console.warn("Affiliate data not found, using default fallback values.");
        // Fallback-Werte
        affiliateUrl = "#";
        streamerName = streamerId;
        videos = [
          "/static/videos/default1.mp4",
          "/static/videos/default2.mp4",
          "/static/videos/default3.mp4"
        ];
      } else {
        // Falls Affiliate-Daten vorhanden sind, verwende diese
        if (data.affiliate_url) {
          affiliateUrl = data.affiliate_url;
        }
        if (data.streamer_name) {
          streamerName = data.streamer_name;
        }
        if (data.videos && Array.isArray(data.videos)) {
          videos = data.videos;
        }
      }

      // Erstelle Carousel-Items aus dem Array 'videos'
      const carouselItems = videos.map(videoSrc => ({
        videoSrc: videoSrc,
        affiliateUrl: affiliateUrl,
        streamerName: streamerName
      }));

      const carouselContainer = document.getElementById("video-carousel");

      // Falls der Container nicht gefunden wurde, logge einen Fehler und beende die Funktion
      if (!carouselContainer) {
        console.error("Carousel container (#video-carousel) not found in the DOM.");
        return;
      }

      // Füge die Carousel-Items in den Container ein
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

      // Nur fortfahren, wenn mindestens ein Carousel-Item existiert
      const items = document.querySelectorAll(".carousel-item");
      if (items.length > 0) {
        let currentIndex = 0;
        setInterval(() => {
          // Sicherheitsabfrage: Falls items.length 0 ist, nichts tun
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
