import DRFSerializer from './drf';

export default DRFSerializer.extend({
  attrs: {
    rockfaces: {embedded: 'always'}
  }
});
