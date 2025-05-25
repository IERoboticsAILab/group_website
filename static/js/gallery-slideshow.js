/**
 * Gallery Slideshow Functionality
 * Provides modal-based image slideshow with navigation controls
 */

class GallerySlideshow {
    constructor() {
        this.currentIndex = 0;
        this.images = [];
        this.modal = null;
        this.slideContainer = null;
        this.slideImage = null;
        this.counter = null;
        this.caption = null;
        this.isOpen = false;
        
        this.init();
    }
    
    init() {
        this.createModal();
        this.bindEvents();
        this.setupGalleryImages();
    }
    
    createModal() {
        // Create modal HTML structure
        const modalHTML = `
            <div id="gallery-slideshow-modal" class="gallery-slideshow-modal">
                <div class="slideshow-container">
                    <button class="slideshow-close" aria-label="Close slideshow">
                        <i class="bi bi-x-lg"></i>
                    </button>
                    <button class="slideshow-nav slideshow-prev" aria-label="Previous image">
                        <i class="bi bi-chevron-left"></i>
                    </button>
                    <img class="slideshow-image" src="" alt="" />
                    <button class="slideshow-nav slideshow-next" aria-label="Next image">
                        <i class="bi bi-chevron-right"></i>
                    </button>
                    <div class="slideshow-counter"></div>
                    <div class="slideshow-caption"></div>
                </div>
            </div>
        `;
        
        // Add modal to body
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Get references to modal elements
        this.modal = document.getElementById('gallery-slideshow-modal');
        this.slideContainer = this.modal.querySelector('.slideshow-container');
        this.slideImage = this.modal.querySelector('.slideshow-image');
        this.counter = this.modal.querySelector('.slideshow-counter');
        this.caption = this.modal.querySelector('.slideshow-caption');
        
        // Get navigation buttons
        this.closeBtn = this.modal.querySelector('.slideshow-close');
        this.prevBtn = this.modal.querySelector('.slideshow-prev');
        this.nextBtn = this.modal.querySelector('.slideshow-next');
    }
    
    bindEvents() {
        // Close button
        this.closeBtn.addEventListener('click', () => this.close());
        
        // Navigation buttons
        this.prevBtn.addEventListener('click', () => this.prev());
        this.nextBtn.addEventListener('click', () => this.next());
        
        // Click outside modal to close
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.close();
            }
        });
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (!this.isOpen) return;
            
            switch(e.key) {
                case 'Escape':
                    this.close();
                    break;
                case 'ArrowLeft':
                    this.prev();
                    break;
                case 'ArrowRight':
                    this.next();
                    break;
            }
        });
        
        // Touch/swipe support
        let startX = 0;
        let endX = 0;
        
        this.slideContainer.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
        });
        
        this.slideContainer.addEventListener('touchend', (e) => {
            endX = e.changedTouches[0].clientX;
            const diff = startX - endX;
            
            if (Math.abs(diff) > 50) { // Minimum swipe distance
                if (diff > 0) {
                    this.next(); // Swipe left - next image
                } else {
                    this.prev(); // Swipe right - previous image
                }
            }
        });
    }
    
    setupGalleryImages() {
        // Find all gallery images and add click handlers
        const galleryImages = document.querySelectorAll('.gallery-img');
        
        galleryImages.forEach((img, index) => {
            // Store image data
            this.images.push({
                src: img.src,
                alt: img.alt,
                caption: this.getImageCaption(img)
            });
            
            // Add click handler
            img.addEventListener('click', () => {
                this.open(index);
            });
            
            // Add visual indicator that image is clickable
            img.style.cursor = 'pointer';
            img.title = 'Click to view in slideshow';
        });
    }
    
    getImageCaption(img) {
        // Try to find caption from various sources
        const nextElement = img.nextElementSibling;
        if (nextElement && (nextElement.classList.contains('text-muted') || nextElement.tagName === 'P')) {
            return nextElement.textContent.trim();
        }
        
        // Check for data attribute
        if (img.dataset.caption) {
            return img.dataset.caption;
        }
        
        // Use alt text as fallback
        return img.alt || '';
    }
    
    open(index = 0) {
        if (this.images.length === 0) return;
        
        this.currentIndex = index;
        this.isOpen = true;
        this.modal.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
        
        this.updateSlide();
        this.updateNavigation();
    }
    
    close() {
        this.isOpen = false;
        this.modal.classList.remove('active');
        document.body.style.overflow = ''; // Restore scrolling
    }
    
    next() {
        if (this.images.length === 0) return;
        
        this.currentIndex = (this.currentIndex + 1) % this.images.length;
        this.updateSlide();
        this.updateNavigation();
    }
    
    prev() {
        if (this.images.length === 0) return;
        
        this.currentIndex = this.currentIndex === 0 ? this.images.length - 1 : this.currentIndex - 1;
        this.updateSlide();
        this.updateNavigation();
    }
    
    updateSlide() {
        const currentImage = this.images[this.currentIndex];
        if (!currentImage) return;
        
        // Add loading state
        this.slideImage.style.opacity = '0.5';
        
        // Update image
        this.slideImage.src = currentImage.src;
        this.slideImage.alt = currentImage.alt;
        
        // Update counter
        this.counter.textContent = `${this.currentIndex + 1} / ${this.images.length}`;
        
        // Update caption
        if (currentImage.caption) {
            this.caption.textContent = currentImage.caption;
            this.caption.style.display = 'block';
        } else {
            this.caption.style.display = 'none';
        }
        
        // Remove loading state when image loads
        this.slideImage.onload = () => {
            this.slideImage.style.opacity = '1';
        };
    }
    
    updateNavigation() {
        // Hide/show navigation buttons based on image count
        if (this.images.length <= 1) {
            this.prevBtn.style.display = 'none';
            this.nextBtn.style.display = 'none';
        } else {
            this.prevBtn.style.display = 'flex';
            this.nextBtn.style.display = 'flex';
        }
    }
}

// Initialize slideshow when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Only initialize if there are gallery images on the page
    if (document.querySelectorAll('.gallery-img').length > 0) {
        new GallerySlideshow();
    }
});

// Export for potential external use
window.GallerySlideshow = GallerySlideshow; 