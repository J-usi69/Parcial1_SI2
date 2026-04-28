import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewRequestCard } from './new-request-card';

describe('NewRequestCard', () => {
  let component: NewRequestCard;
  let fixture: ComponentFixture<NewRequestCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NewRequestCard],
    }).compileComponents();

    fixture = TestBed.createComponent(NewRequestCard);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
