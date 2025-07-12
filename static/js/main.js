const carousel = document.querySelector('.carousel');
if (carousel) {
    let currentIndex = 0;
    const items = carousel.querySelectorAll('.carousel-item');
    
    function showItem(index) {
        items.forEach((item, i) => {
            item.style.display = i === index ? 'block' : 'none';
        });
    }
    
    function nextItem() {
        currentIndex = (currentIndex + 1) % items.length;
        showItem(currentIndex);
    }
    
    setInterval(nextItem, 5000);
}

document.querySelectorAll('.image-gallery').forEach(gallery => {
    gallery.addEventListener('click', (e) => {
        if (e.target.classList.contains('gallery-item')) {
            const imageUrl = e.target.getAttribute('data-image');
            const lightbox = document.createElement('div');
            lightbox.className = 'lightbox';
            lightbox.innerHTML = `
                <img src="${imageUrl}" alt="Gallery Image" class="lightbox-image">
                <button class="lightbox-close">&times;</button>
            `;
            document.body.appendChild(lightbox);
            
            lightbox.querySelector('.lightbox-close').addEventListener('click', () => {
                lightbox.remove();
            });
        }
    });
});

document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', (e) => {
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                field.classList.add('is-invalid');
                isValid = false;
            } else {
                field.classList.remove('is-invalid');
            }
        });
        
        if (!isValid) {
            e.preventDefault();
        }
    });
});

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
