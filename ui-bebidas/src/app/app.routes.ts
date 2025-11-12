import { Routes } from '@angular/router';
import { MenuListComponent } from './components/menu-list/menu-list.component';
import { AddBebidaComponent } from './components/add-bebida/add-bebida.component';

export const routes: Routes = [
  { path: '', redirectTo: '/menu', pathMatch: 'full' },
  { path: 'menu', component: MenuListComponent },
  { path: 'add', component: AddBebidaComponent }
];
