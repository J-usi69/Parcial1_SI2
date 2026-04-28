import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewBranchForm } from './new-branch-form';

describe('NewBranchForm', () => {
  let component: NewBranchForm;
  let fixture: ComponentFixture<NewBranchForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NewBranchForm],
    }).compileComponents();

    fixture = TestBed.createComponent(NewBranchForm);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
