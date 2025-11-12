import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

export interface Notification {
  id: number;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  duration?: number;
}

@Injectable({
  providedIn: 'root'
})
export class NotificationService {
  private notifications$ = new BehaviorSubject<Notification[]>([]);
  private idCounter = 0;

  getNotifications() {
    return this.notifications$.asObservable();
  }

  show(type: Notification['type'], message: string, duration = 5000) {
    const notification: Notification = {
      id: ++this.idCounter,
      type,
      message,
      duration
    };

    const currentNotifications = this.notifications$.value;
    this.notifications$.next([...currentNotifications, notification]);

    if (duration > 0) {
      setTimeout(() => {
        this.remove(notification.id);
      }, duration);
    }

    return notification.id;
  }

  remove(id: number) {
    const currentNotifications = this.notifications$.value;
    this.notifications$.next(currentNotifications.filter(n => n.id !== id));
  }

  success(message: string, duration?: number) {
    return this.show('success', message, duration);
  }

  error(message: string, duration?: number) {
    return this.show('error', message, duration);
  }

  warning(message: string, duration?: number) {
    return this.show('warning', message, duration);
  }

  info(message: string, duration?: number) {
    return this.show('info', message, duration);
  }
}