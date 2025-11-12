import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BebidaService, Bebida } from '../../services/bebida.service';

@Component({
  selector: 'app-menu-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './menu-list.component.html',
  styleUrls: ['./menu-list.component.css']
})
export class MenuListComponent implements OnInit {
  bebidas: Bebida[] = [];
  loading = false;
  error: string | null = null;

  constructor(private bebidaService: BebidaService) { }

  ngOnInit(): void {
    this.loadMenu();
  }

  loadMenu(): void {
    this.loading = true;
    this.bebidaService.getMenu().subscribe({
      next: (data) => {
        this.bebidas = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = err.message;
        this.loading = false;
      }
    });
  }
}