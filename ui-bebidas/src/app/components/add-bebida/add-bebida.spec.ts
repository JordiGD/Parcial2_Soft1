import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';

import { AddBebidaComponent } from './add-bebida.component';

describe('AddBebidaComponent', () => {
  let component: AddBebidaComponent;
  let fixture: ComponentFixture<AddBebidaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AddBebidaComponent],
      providers: [provideHttpClient()]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddBebidaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
