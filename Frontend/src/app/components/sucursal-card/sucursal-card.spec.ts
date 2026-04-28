import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SucursalCard } from './sucursal-card';

describe('SucursalCard', () => {
  let component: SucursalCard;
  let fixture: ComponentFixture<SucursalCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SucursalCard],
    }).compileComponents();

    fixture = TestBed.createComponent(SucursalCard);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
