import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { BebidaService, Bebida } from './bebida.service';

describe('BebidaService', () => {
  let service: BebidaService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        BebidaService,
        provideHttpClient()
      ]
    });
    service = TestBed.inject(BebidaService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should have correct API URL', () => {
    expect((service as any).apiUrl).toBe('http://localhost:8001/menu');
  });
});