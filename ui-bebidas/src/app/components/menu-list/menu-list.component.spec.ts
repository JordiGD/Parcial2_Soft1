import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { of, throwError } from 'rxjs';
import { MenuListComponent } from './menu-list.component';
import { BebidaService, Bebida } from '../../services/bebida.service';

describe('MenuListComponent', () => {
  let component: MenuListComponent;
  let fixture: ComponentFixture<MenuListComponent>;
  let bebidaService: jasmine.SpyObj<BebidaService>;

  beforeEach(async () => {
    const bebidaServiceSpy = jasmine.createSpyObj('BebidaService', ['getMenu']);

    await TestBed.configureTestingModule({
      imports: [ MenuListComponent ],
      providers: [
        provideHttpClient(),
        { provide: BebidaService, useValue: bebidaServiceSpy }
      ]
    }).compileComponents();

    bebidaService = TestBed.inject(BebidaService) as jasmine.SpyObj<BebidaService>;
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MenuListComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load menu on init', () => {
    const mockBebidas: Bebida[] = [
      { id: 1, name: 'Latte', size: 'medium' as const, price: 3.50 }
    ];
    bebidaService.getMenu.and.returnValue(of(mockBebidas));

    fixture.detectChanges();

    expect(component.bebidas).toEqual(mockBebidas);
    expect(component.loading).toBeFalse();
  });

  it('should handle error when loading menu', () => {
    bebidaService.getMenu.and.returnValue(throwError(() => new Error('Error')));

    fixture.detectChanges();

    expect(component.error).toBe('Error al cargar el menú');
    expect(component.loading).toBeFalse();
  });
});