import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IncidentConsultComponent } from './incident-consult.component';

describe('IncidentConsultComponent', () => {
  let component: IncidentConsultComponent;
  let fixture: ComponentFixture<IncidentConsultComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [IncidentConsultComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(IncidentConsultComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
