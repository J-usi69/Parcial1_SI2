import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GridColumn } from './grid-column';

describe('GridColumn', () => {
  let component: GridColumn;
  let fixture: ComponentFixture<GridColumn>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GridColumn],
    }).compileComponents();

    fixture = TestBed.createComponent(GridColumn);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
