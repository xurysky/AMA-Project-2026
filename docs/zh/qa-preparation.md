# Q&A 准备 — Panel 可能问的 10 个问题

## Q1: 为什么选优衣库而不是其他零售商？

**回答要点：**
- **数据基础最好**：RFID 全覆盖 + "管理驾驶舱"3000万+数据点
- **规模够大**：3500+门店、13亿件年产量、2亿+粉丝
- **亚洲核心**：中国900+门店、日本破万亿日元
- **Agent 就绪度最高**：有数据基础但还没实现 Agent 化 = 机会窗口
- **数字化转型标杆**：Ariake Project 供应链自动化、大数据需求预测

## Q2: 5 个 Agent 是架构图还是可运行的产品？

**回答要点：**
- 本项目是 **架构设计 + 原型验证**，不是完整产品
- 每个 Agent 有明确的输入/输出/技术栈
- 场景演示验证了 Agent 间协作的可行性
- 实际部署需要 6-12 个月的工程化
- 参考了 Azure AI Foundry 的生产级架构

## Q3: 预期效果的数据从哪来？

**回答要点：**
- +40% 销售：McKinsey 研究（AI 个性化提升 20-35% 转化率）+ 优衣库现有增长趋势
- -50% 库存：Gartner 研究（AI 需求预测减少 20-50% 库存）
- 85% 满意度：Forrester 研究（AI 客服提升 25% 满意度）
- +60% CLV：Harvard 研究（个性化提升 40% CLV）
- 这些是行业基准，不是我们自己编的

## Q4: 亚洲特殊性怎么落地？

**回答要点：**
- **隐私合规**：合成 Persona（TT205）解决冷启动 + 数据本地化存储（Cosmos DB 亚太区域）
- **多语言**：LLM 天然多语言能力 + Agent 语言偏好配置
- **支付适配**：MCP 协议统一 API 接口（APIM 网关）
- **城乡差异**：Agent 根据门店位置调整策略（一线 vs 三四线）

## Q5: 为什么不用现有的推荐系统？

**回答要点：**
- 现有系统是**单点工具**（推荐引擎、库存系统、定价系统各自独立）
- Agent 架构的核心价值是**跨系统协作**和**自主决策**
- 例如：库存 Agent 发现某 SKU 库存过高 → 自动通知 Pricing Agent 调价 → 通知 Marketing Agent 推促销
- 这种**端到端自主协作**是传统系统做不到的

## Q6: 技术风险有哪些？

**回答要点：**
- **幻觉风险**：LLM 可能生成错误建议 → 用 RAG + 事实检查缓解
- **延迟风险**：Agent 间通信可能延迟 → 用事件驱动 + 缓存优化
- **成本风险**：LLM 调用成本高 → 用小模型处理简单任务，大模型只做推理
- **合规风险**：数据隐私 → 合成 Persona + 数据本地化

## Q7: 成本估算？

**回答要点：**
- Azure OpenAI：~$500/月（GPT-4o，中等使用量）
- Cosmos DB：~$200/月（Serverless）
- Azure ML：~$300/月（Standard）
- Event Hubs：~$100/月
- 其他：~$200/月
- **总计：~$1,300/月**（原型阶段）
- 生产环境需要 10-50x 扩展

## Q8: 为什么选 Azure 而不是 AWS/GCP？

**回答要点：**
- **AI 生态完整**：Azure OpenAI + AI Foundry + ML + Cosmos DB 一站式
- **企业级安全**：Entra ID + Purview + Defender
- **混合云能力**：Arc + 自托管网关
- **亚洲覆盖**：东亚/东南亚区域完善
- **成本优势**：Visual Studio Enterprise 订阅有折扣

## Q9: 如何衡量成功？

**回答要点：**
- **量化指标**：销售增长、库存周转率、客户满意度、CLV
- **A/B 测试**：Agent 组 vs 对照组
- **业务指标**：转化率、客单价、复购率
- **技术指标**：响应时间、准确率、可用性

## Q10: 下一步计划？

**回答要点：**
- **短期**（3 个月）：MVP 部署，覆盖 10 家门店
- **中期**（6 个月）：扩展到 100 家门店，优化 Agent 协作
- **长期**（12 个月）：全渠道覆盖，Agent 自主决策
- **关键里程碑**：POC → MVP → Beta → GA

## Q11: Agent 之间怎么协作？（Agentic Behavior — 评审重点）

**回答要点：**
- **Handoff 模式**：Inventory Agent 发现库存过高 → 通过 A2A Protocol 通知 Pricing Agent → Pricing Agent 返回调价建议 → Inventory Agent 确认执行
- **Reflection 模式**：Marketing Agent 执行营销活动后，Customer Understanding Agent 分析效果反馈，Marketing Agent 据此调整策略
- **State Graph**：所有 Agent 共享客户状态图，任何 Agent 的决策都会更新状态，其他 Agent 实时感知
- **协调机制**：Azure AI Foundry 作为 Orchestrator，管理 Agent 间的任务分配和优先级
- **Human-in-the-Loop**：关键决策（如大幅调价、大规模营销）需要人工确认

## Q12: 安全怎么保证？（Security — 评审重点）

**回答要点：**
- **身份管理**：Azure Entra ID + Managed Identity，每个 Agent 有独立身份和最小权限
- **数据保护**：Azure Purview 数据分类 + Cosmos DB 加密（静态+传输）+ 数据本地化
- **网络安全**：Private Endpoints + Azure Front Door WAF + DDoS 防护
- **AI 安全**：输入验证 + Prompt Injection 检测 + 输出过滤 + OWASP Top 10 合规
- **增量实施**：Phase 1 基础安全 → Phase 2 身份与合规 → Phase 3 零信任
- **合成 Persona**：客户理解 Agent 使用合成数据解决冷启动，不暴露真实客户 PII

## Q13: CI/CD 和运维怎么做？（CI/CD + Day 2 Ops — 评审重点）

**回答要点：**
- **CI/CD 流水线**：GitHub Actions 自动化 → 代码质量检查 → 安全扫描 → 测试 → 构建 → 金丝雀部署（5%流量）→ 全量发布
- **分支保护**：main 分支需要 PR + 审核 + 通过所有检查
- **部署策略**：金丝雀部署 + 自动回滚（错误率>0.1%或延迟p95>2s自动回滚）
- **Day 2 运维**：配置管理（Azure App Configuration）+ Feature Flags + A/B 测试 + 容量规划
- **事件响应**：P1（15分钟响应）→ P2（1小时）→ P3（4小时），事后复盘

## Q14: 系统出故障了怎么办？（Reliability — 评审重点）

**回答要点：**
- **高可用**：每个 Agent 3 副本 + 跨可用区部署 + Cosmos DB 多区域复制
- **熔断器**：连续 5 次失败 → 自动熔断 → 30秒后半开测试 → 恢复后自动关闭
- **优雅降级**：非关键 Agent 故障时跳过（Marketing Agent 故障不影响定价）
- **灾难恢复**：RPO < 5分钟，RTO < 30分钟，季度 DR 演练
- **具体场景**：Azure OpenAI 超时 → 使用缓存推荐 → 重试 → 降级到规则引擎

## Q15: 这个方案跟竞品（Google/AWS）比有什么优势？

**回答要点：**
- **Azure OpenAI 独占**：GPT-4o 只在 Azure 上提供企业级 SLA
- **AI Foundry**：一站式 Agent 开发+部署+监控，Google/AWS 没有等价产品
- **Fabric 数据平台**：OneLake 统一数据湖，比 BigQuery/Redshift 更集成
- **安全合规**：Entra ID + Purview + Defender 三位一体，企业客户首选
- **亚洲覆盖**：东亚/东南亚区域多，数据本地化合规
- **混合云**：Arc 支持混合部署，适合有本地需求的零售客户

---

## C-suite 角色速查表

| 角色 | 关注点 | 准备方向 |
|------|--------|----------|
| **CEO** | ROI、业务价值、竞争差异 | "投入多少？多久回本？跟竞品比？" |
| **CFO** | 成本控制、预算、TCO | "总成本多少？怎么分阶段投入？" |
| **CTO** | 架构、可扩展性、技术选型 | "为什么选这个架构？怎么扩展？" |
| **CISO** | 安全、合规、数据隐私 | "数据怎么保护？合规怎么做？" |
| **COO** | Day 2 Ops、运维、部署 | "怎么更新？出问题怎么回滚？" |
