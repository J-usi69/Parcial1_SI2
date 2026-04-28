import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewUserForm } from './new-user-form';

describe('NewUserForm', () => {
  let component: NewUserForm;
  let fixture: ComponentFixture<NewUserForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NewUserForm],
    }).compileComponents();

    fixture = TestBed.createComponent(NewUserForm);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
