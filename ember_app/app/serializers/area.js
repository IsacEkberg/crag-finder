import DRFSerializer from './drf';

export default DRFSerializer.extend({
  attrs: {
    rockface: {embedded: 'always'}
  }
});
