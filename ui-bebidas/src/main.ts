import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { App } from './app/app';

// Suprimir warnings de desarrollo en producción
if (typeof window !== 'undefined' && window.location.hostname !== 'localhost') {
  console.warn = () => {};
  console.info = () => {};
}

bootstrapApplication(App, appConfig)
  .catch((err) => {
    // Solo mostrar errores críticos en desarrollo
    if (typeof window !== 'undefined' && window.location.hostname === 'localhost') {
      console.error('Error al inicializar la aplicación:', err);
    }
  });
