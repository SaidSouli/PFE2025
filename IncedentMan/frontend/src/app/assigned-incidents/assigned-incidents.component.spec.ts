import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AssignedIncidentsComponent } from './assigned-incidents.component';

describe('AssignedIncidentsComponent', () => {
  let component: AssignedIncidentsComponent;
  let fixture: ComponentFixture<AssignedIncidentsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AssignedIncidentsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AssignedIncidentsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
