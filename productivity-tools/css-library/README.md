# CSS Library - ThemeCT

A comprehensive CSS framework optimized for creating modern, responsive web interfaces with professional branding.

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/CSS-Modern-green.svg" alt="CSS">
  <img src="https://img.shields.io/badge/Responsive-Yes-brightgreen.svg" alt="Responsive">
</p>

## Features

### Design System
- **CSS Variables** for consistent theming
- **Professional color palette** with primary green (#229174)
- **Modern shadows and gradients**
- **Responsive typography system**

### Components
- **Modern Cards** with hover effects and gradients
- **Navigation sidebar** with collapsible sections
- **Buttons and badges** with multiple variants
- **Grid systems** for responsive layouts
- **Form elements** styled consistently

### Layout System
- **Fixed header banner** with logo placement
- **Sidebar navigation** with smooth animations
- **Main content area** with optimal spacing
- **Mobile-first responsive** design

## Quick Start

### Basic Usage

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Project</title>
    <link rel="stylesheet" href="path/to/themeCT.css">
</head>
<body>
    <!-- Your content here -->
</body>
</html>
```

### CDN Usage (when published)

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/your-username/dev-tools-collection@main/productivity-tools/css-library/styles/themeCT.css">
```

## Components

### Cards

```html
<!-- Modern Card -->
<div class="modern-card">
    <div class="modern-card-halo-1"></div>
    <div class="modern-card-halo-2"></div>
    <div class="modern-card-header">
        <div class="modern-card-icon">
            <i class="fas fa-star"></i>
        </div>
        <h3 class="modern-card-title">Card Title</h3>
    </div>
    <div class="modern-card-content">
        <p>Card content goes here.</p>
    </div>
</div>

<!-- Standard Card with Variants -->
<div class="card card-primary">
    <div class="card-header">
        <div class="card-icon">
            <i class="fas fa-info"></i>
        </div>
        <h4 class="card-title">Information</h4>
    </div>
    <div class="card-body">
        <p>Card content with primary styling.</p>
    </div>
</div>
```

### Buttons

```html
<!-- Primary Button -->
<a href="#" class="btn">
    <i class="fas fa-download"></i>
    Primary Action
</a>

<!-- Outline Button -->
<a href="#" class="btn btn-outline">
    <i class="fas fa-edit"></i>
    Secondary Action
</a>

<!-- Professional Styled Button -->
<a href="#" class="green-button">
    <i class="fas fa-arrow-right"></i>
    Learn More
</a>
```

### Navigation

```html
<nav class="sidebar">
    <ul class="sidebar-nav">
        <li class="sidebar-nav-item">
            <a href="#" class="sidebar-nav-link active">
                Home
                <span class="toggle-btn">▼</span>
            </a>
            <ul class="sidebar-subnav">
                <li><a href="#" class="sidebar-subnav-link">Overview</a></li>
                <li><a href="#" class="sidebar-subnav-link">Getting Started</a></li>
            </ul>
        </li>
    </ul>
</nav>
```

### Grid System

```html
<!-- Responsive Grid -->
<div class="responsive-grid">
    <div class="grid-item">
        <div class="grid-item-content">
            <div class="grid-item-icon">
                <i class="fas fa-cog"></i>
            </div>
            <h4 class="grid-item-title">Feature 1</h4>
            <p class="grid-item-description">Description here.</p>
        </div>
    </div>
    <!-- More grid items -->
</div>

<!-- Flexible Layout -->
<div class="responsive-flex">
    <div class="responsive-flex-item">Content 1</div>
    <div class="responsive-flex-item">Content 2</div>
</div>
```

## CSS Variables

### Color Palette

```css
:root {
    /* Primary Colors */
    --color-primary: #229174;
    --color-primary-dark: #1a7a5e;
    --color-primary-light: #8fd9be;
    --color-primary-very-light: #e8f5f0;
    
    /* Secondary Colors */
    --color-secondary: #3498db;
    --color-warning: #f39c12;
    --color-danger: #e74c3c;
    
    /* Text Colors */
    --color-text: #364145;
    --color-text-light: #4a5568;
    --color-text-lighter: #7f8c8d;
}
```

### Spacing System

```css
:root {
    --spacing-xs: 5px;
    --spacing-sm: 10px;
    --spacing-md: 15px;
    --spacing-lg: 20px;
    --spacing-xl: 30px;
}
```

### Border Radius

```css
:root {
    --border-radius-sm: 4px;
    --border-radius-md: 8px;
    --border-radius-lg: 12px;
    --border-radius-circle: 50%;
}
```

## Customization

### Override Variables

```css
:root {
    /* Custom primary color */
    --color-primary: #your-color;
    
    /* Custom spacing */
    --spacing-lg: 25px;
    
    /* Custom shadows */
    --shadow-lg: 0 15px 40px rgba(0,0,0,0.1);
}
```

### Add Custom Components

```css
.my-custom-card {
    background: var(--color-card-bg);
    border-radius: var(--border-radius-lg);
    padding: var(--spacing-lg);
    box-shadow: var(--shadow-md);
    transition: var(--transition-normal);
}

.my-custom-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-hover);
}
```

## Responsive Breakpoints

```css
/* Large screens */
@media (max-width: 1200px) { /* Styles */ }

/* Medium to large screens */
@media (min-width: 769px) and (max-width: 992px) { /* Styles */ }

/* Mobile */
@media (max-width: 768px) { /* Styles */ }

/* Small mobile */
@media (max-width: 480px) { /* Styles */ }

/* Very small mobile */
@media (max-width: 320px) { /* Styles */ }
```

## Utility Classes

### Classification Badges

```html
<span class="classification-public">Public</span>
<span class="classification-internal">Internal</span>
<span class="classification-confidential">Confidential</span>
<span class="classification-secret">Secret</span>
```

### Severity Indicators

```html
<span class="incident-severity severity-critical">Critical</span>
<span class="incident-severity severity-high">High</span>
<span class="incident-severity severity-medium">Medium</span>
<span class="incident-severity severity-low">Low</span>
```

### Badges

```html
<span class="badge badge-primary">Primary</span>
<span class="badge badge-secondary">Secondary</span>
<span class="badge badge-warning">Warning</span>
<span class="badge badge-danger">Danger</span>
```

## Best Practices

### Performance
- **CSS variables** for easy theming
- **Minimal specificity** for easy overrides
- **Optimized animations** with hardware acceleration
- **Mobile-first** responsive design

### Accessibility
- **High contrast** color combinations
- **Focus states** for keyboard navigation
- **Screen reader** friendly markup
- **Semantic HTML** structure

### Maintenance
- **Modular CSS** structure
- **Consistent naming** conventions
- **Well-documented** variables
- **Backwards compatible** updates

## Browser Support

- **Chrome** 70+
- **Firefox** 65+
- **Safari** 12+
- **Edge** 79+
- **Mobile browsers** (iOS Safari, Chrome Mobile)

## File Structure

```
css-library/
├── styles/
│   ├── themeCT.css              # Complete theme
│   └── themes/                  # Additional themes (future)
├── examples/
│   ├── basic-layout.html        # Basic usage example
│   ├── components-demo.html     # Components showcase
│   └── responsive-demo.html     # Responsive layout demo
└── README.md                    # This file
```

## Contributing

When adding new components or modifying existing ones:

1. **Follow the existing variable system**
2. **Maintain responsive design principles**
3. **Test across different browsers**
4. **Update documentation and examples**
5. **Use semantic CSS class names**

## Changelog

### Version 1.0.0
- Initial release with professional theme
- Complete component library
- Responsive design system
- Modern card components
- Navigation system
- Grid and flex utilities

## License

This CSS library is part of the dev-tools-collection and is licensed under the MIT License.

---

**Professional CSS framework optimized for modern web development.**