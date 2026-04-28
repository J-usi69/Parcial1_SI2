import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewRequests } from './new-requests';

describe('NewRequests', () => {
  let component: NewRequests;
  let fixture: ComponentFixture<NewRequests>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NewRequests],
    }).compileComponents();

    fixture = TestBed.createComponent(NewRequests);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
