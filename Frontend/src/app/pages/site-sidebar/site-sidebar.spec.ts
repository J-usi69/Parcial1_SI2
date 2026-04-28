import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SiteSidebar } from './site-sidebar';

describe('SiteSidebar', () => {
  let component: SiteSidebar;
  let fixture: ComponentFixture<SiteSidebar>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SiteSidebar],
    }).compileComponents();

    fixture = TestBed.createComponent(SiteSidebar);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
