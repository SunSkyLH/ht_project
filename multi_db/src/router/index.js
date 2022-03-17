import Vue from 'vue'
import Router from 'vue-router'
import AbnormalDetection from '../components/AbnormalDetection'
import FaultPropagation from '../components/FaultPropagation'
import ModuleIntegration from '../components/ModuleIntegration'
import Introduction from '../components/Introduction'
import Instruction from '../components/Instruction'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/Introduction',
      name: 'Introduction',
      component: Introduction
    },{
      path: '/Instruction',
      name: 'Instruction',
      component: Instruction
    },
    {
      path: '/AbnormalDetection',
      name: 'AbnormalDetection',
      component: AbnormalDetection
    },
    {
      path: '/FaultPropagation',
      name: 'FaultPropagation',
      component: FaultPropagation
    },
    {
      path: '/ModuleIntegration',
      name: 'ModuleIntegration',
      component: ModuleIntegration,
    },



  ]
})
