# AMA
<!-- impeccable:product-schema 1 -->
## Platform
web
## Users
企业客户演示观众，以及讲解AMA的演示者。
## Product Purpose
围绕零售业务案例呈现专业Agent如何形成受规则约束、可人工审批的经营方案。
## Capabilities and Constraints
现有业务平台继续运行；本次扩展为独立Agent Framework + Durable试用入口。用户要求先部署看看，完成后同步AMA代码仓库。仅用标明的虚构库存案例，不执行真实调拨或营销发送。运行图反映真实状态，不提供拖拽编辑器，不宣称A2A已实现。
## Evidence on Hand
src/retail_case_engine.py的积压案例；docs/design/agent-framework-durable-proposal-20261103.md。
## Product Principles
- 规则与模型生成明确区分。
- 审批不等于执行。
- 页面只展示实际状态和可核对产出。
