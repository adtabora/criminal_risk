import { Component } from '@angular/core';
import { MapService } from '../services/map.service';
declare var google: any;

@Component({
  selector: 'map',
  providers: [MapService],
  // styleUrls: ['./map.styles.css'],
  template: `

  <div>
      Soon a Map will appear here
  </div>

  <div id="floating-panel">
      <button md-button md-raised-button (click)="showTrain()" color="none">
        Train
      </button>
      <button md-button md-raised-button (click)="showTest()" color="none">
        Test
      </button>
  </div>
  <div id="map"></div>
    `,
    styles:[`
    #map {
        height: 300px;
      }
    #floating-panel {
        background-color: rgba(182, 182, 182, 0.40);
        border: 1px solid #999;
        right: 10px;
        padding: 5px;
        position: absolute;
        top: 100px;
        z-index: 5;
      }
    `]
  

})

export class MapComponent {

  lat: number = 14.089507;
  lng: number = -87.1771873;
  zoom: number = 12;

  map: any;
  heatmap: any; 

  points: any[];

  constructor(private mapService: MapService) { }

  ngOnInit() {
    this.map = new google.maps.Map(document.getElementById('map'), {
          zoom: this.zoom,
          center: {lat: this.lat, lng: this.lng}
        });  

    this.heatmap = new google.maps.visualization.HeatmapLayer({
      data: [],
      map: this.map,
      radius: 16
    });

    this.listPoints();

    
  }

  renderHeatmap() {
    var heatPoints = <any>[]
    this.points.forEach(point => {
      heatPoints.push( new google.maps.LatLng(point.lat, point.long) )
    });


    this.heatmap.setData( heatPoints)

  }

  listPoints(){
    var self = this
    this.mapService.listPoints().then(function(response){
        self.points = response
        self.renderHeatmap()
    });
  }

  


  
  
}
