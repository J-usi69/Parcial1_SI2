import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RequestCardComponent } from './request-card';

describe('RequestCard', () => {
  let component: RequestCardComponent;
  let fixture: ComponentFixture<RequestCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RequestCardComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(RequestCardComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    // Asignar datos ANTES de detectar cambios
    component.data = {
      tipo: 'Prueba',
      titulo: 'Test',
      tiempo: 'Ahora',
      usuario: 'User',
      ubicacion: 'Loc',
    };
    fixture.detectChanges();
    expect(component).toBeTruthy();
  });
});
