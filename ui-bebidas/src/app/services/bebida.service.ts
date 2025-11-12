import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Bebida {
  id?: number;
  name: string;
  size: 'small' | 'medium' | 'large';
  price: number;
}

@Injectable({
  providedIn: 'root'
})
export class BebidaService {
  private apiUrl = 'http://localhost:8001/menu';

  constructor(private http: HttpClient) { }

  getMenu(): Observable<Bebida[]> {
    return this.http.get<Bebida[]>(this.apiUrl);
  }

  addBebida(bebida: Bebida): Observable<Bebida> {
    return this.http.post<Bebida>(this.apiUrl, bebida);
  }

  getBebidaByName(name: string): Observable<Bebida> {
    return this.http.get<Bebida>(`${this.apiUrl}/${name}`);
  }
}