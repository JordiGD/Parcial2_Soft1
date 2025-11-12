import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BebidaService, Bebida } from '../../services/bebida.service';

@Component({
  selector: 'app-add-bebida',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './add-bebida.component.html',
  styleUrls: ['./add-bebida.component.css']
})
export class AddBebidaComponent {
  bebida: Bebida = {
    name: '',
    size: 'medium',
    price: 0
  };
  
  success = false;
  error: string | null = null;

  constructor(private bebidaService: BebidaService) { }

  onSubmit(): void {
    this.success = false;
    this.error = null;
    
    this.bebidaService.addBebida(this.bebida).subscribe({
      next: (data) => {
        this.success = true;
        this.bebida = { name: '', size: 'medium', price: 0 };
        setTimeout(() => this.success = false, 3000);
      },
      error: (err) => {
        this.error = err.message;
      }
    });
  }
}