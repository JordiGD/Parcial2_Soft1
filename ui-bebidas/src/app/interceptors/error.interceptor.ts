import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { catchError, throwError } from 'rxjs';

export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      let errorMessage = 'Ha ocurrido un error';
      
      if (error.error instanceof ErrorEvent) {
        // Error del lado del cliente
        errorMessage = error.error.message;
      } else {
        // Error del servidor
        switch (error.status) {
          case 404:
            errorMessage = 'Recurso no encontrado';
            break;
          case 500:
            errorMessage = 'Error interno del servidor';
            break;
          case 0:
            errorMessage = 'No se puede conectar al servidor. Verifique que la API esté ejecutándose.';
            break;
          default:
            errorMessage = error.error?.detail || error.message || 'Error desconocido';
        }
      }
      
      // Log detallado solo en desarrollo (no mostrar en producción)
      if (typeof window !== 'undefined' && window.location.hostname === 'localhost') {
        console.error('HTTP Error:', error);
      }
      
      return throwError(() => new Error(errorMessage));
    })
  );
};