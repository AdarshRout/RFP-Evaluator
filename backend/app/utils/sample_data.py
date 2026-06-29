"""
Sample RFP and Proposal documents for demonstration.
Based on a realistic Cloud ERP Implementation RFP scenario.
"""

SAMPLE_RFP = """
REQUEST FOR PROPOSAL (RFP)
Cloud ERP Implementation for Global Manufacturing Operations
RFP Reference: RFP-2024-ERP-001

SECTION 1: PROJECT OVERVIEW
TechManufacture Corp. seeks proposals from qualified vendors for end-to-end implementation of a Cloud ERP system across 12 global sites. The project involves migrating from legacy SAP on-premise to a cloud-native ERP solution.

SECTION 2: TECHNICAL REQUIREMENTS
REQ-T1: The solution must be cloud-native, supporting multi-cloud deployment (AWS, Azure, or GCP).
REQ-T2: Real-time integration with existing IoT sensors and manufacturing execution systems (MES).
REQ-T3: API-first architecture with REST and GraphQL endpoints for all core modules.
REQ-T4: Minimum 99.9% system uptime SLA with disaster recovery RTO < 4 hours.
REQ-T5: Support for 5,000+ concurrent users across global locations.
REQ-T6: Mobile-first interface supporting iOS and Android for shop floor operations.
REQ-T7: AI/ML capabilities for predictive maintenance, demand forecasting, and inventory optimization.

SECTION 3: DATA & SECURITY REQUIREMENTS
REQ-S1: GDPR, SOC 2 Type II, and ISO 27001 compliance mandatory.
REQ-S2: Data residency controls allowing regional data segregation per local regulations.
REQ-S3: End-to-end encryption for data at rest and in transit (AES-256).
REQ-S4: Role-based access control (RBAC) with multi-factor authentication.
REQ-S5: Complete audit trail with 7-year data retention capability.

SECTION 4: IMPLEMENTATION & TIMELINE
REQ-I1: Full implementation must be completed within 18 months from contract signing.
REQ-I2: Phased rollout plan required: Pilot (3 months) → Regional (6 months) → Global (9 months).
REQ-I3: Zero production downtime migration strategy mandatory.
REQ-I4: Comprehensive training program for 500+ end users.
REQ-I5: Dedicated project manager with PMP certification required.

SECTION 5: FINANCIAL REQUIREMENTS
REQ-F1: Total cost of ownership (TCO) for 5 years must be submitted.
REQ-F2: Fixed-price contract with defined milestones and payment schedule.
REQ-F3: Implementation cost not to exceed $5 million USD.
REQ-F4: Annual maintenance and support cost breakdown required.
REQ-F5: Performance-based payment terms linked to milestone delivery.

SECTION 6: VENDOR QUALIFICATIONS
REQ-V1: Minimum 10 years experience in ERP implementation.
REQ-V2: At least 3 reference implementations in manufacturing sector (Fortune 500 preferred).
REQ-V3: Certified partnership with at least one major cloud provider.
REQ-V4: Local support presence in minimum 8 of 12 target countries.
REQ-V5: ISO 9001 quality management certification.

SECTION 7: SUPPORT & MAINTENANCE
REQ-M1: 24/7 support with 4-hour response SLA for critical issues.
REQ-M2: Dedicated customer success manager post go-live for 12 months.
REQ-M3: Quarterly system health reviews and optimization recommendations.
"""

SAMPLE_PROPOSAL = """
PROPOSAL RESPONSE
TechSolutions Global Inc. — Cloud ERP Implementation Proposal
Response to RFP-2024-ERP-001
Submitted: November 15, 2024

EXECUTIVE SUMMARY
TechSolutions Global Inc. is proud to present this comprehensive proposal for TechManufacture Corp.'s Cloud ERP transformation initiative. With 15 years of ERP implementation experience and over 200 successful deployments, we are uniquely positioned to deliver this mission-critical project.

SECTION 1: TECHNICAL SOLUTION

Cloud Architecture:
Our proposed solution leverages a cloud-native microservices architecture deployed on AWS (primary) with Azure as failover. The platform is built on Kubernetes for container orchestration, ensuring elastic scalability. We support multi-cloud deployment and can accommodate GCP if required.

API Architecture:
Our platform provides comprehensive REST API coverage for all modules with OpenAPI 3.0 documentation. GraphQL support is available for flexible data querying. We maintain a developer portal with SDKs in 6 programming languages.

Scalability & Performance:
The platform has been load-tested to support 10,000 concurrent users with sub-200ms response times. Our SLA guarantees 99.95% uptime, exceeding the minimum 99.9% requirement. Disaster recovery RTO is 2 hours with RPO of 15 minutes.

IoT Integration:
We have pre-built connectors for 50+ MES systems and IoT platforms including Siemens MindSphere, PTC ThingWorx, and custom MQTT/OPC-UA protocols. Real-time data streaming is handled through Apache Kafka.

Mobile Experience:
Our mobile application (iOS/Android) is specifically designed for manufacturing environments with offline capability, barcode scanning, and voice commands for hands-free shop floor operations.

AI/ML Capabilities:
Integrated AI modules include:
- PredictPro: Predictive maintenance using equipment sensor data (95% accuracy in trials)
- DemandAI: Demand forecasting with 18-month horizon and 92% accuracy
- InventoryOptimizer: Real-time inventory optimization reducing carrying costs by 23% on average

SECTION 2: SECURITY & COMPLIANCE

Certifications:
TechSolutions holds SOC 2 Type II certification (renewed annually), ISO 27001 certification, and is GDPR-compliant by design. We are in final stages of completing our FedRAMP authorization.

Data Residency:
Our platform supports fine-grained data residency controls with dedicated regional data centers in EU (Frankfurt, Dublin), Americas (Virginia, São Paulo), and APAC (Singapore, Tokyo, Sydney). Data never crosses regional boundaries without explicit customer authorization.

Encryption & Access:
All data encrypted with AES-256 at rest and TLS 1.3 in transit. Our RBAC system supports hierarchical roles with attribute-based access control (ABAC) for complex manufacturing environments. MFA is enforced for all user accounts with support for hardware security keys.

Audit Trail:
Comprehensive audit logging captures all system events with tamper-proof storage. We retain audit logs for 10 years, exceeding the 7-year requirement.

SECTION 3: IMPLEMENTATION APPROACH

Timeline: We commit to completing the full implementation within 16 months, 2 months ahead of the 18-month requirement.

Phase 1 - Pilot (Months 1-3): Deploy at 2 pilot sites with core financials and inventory modules. Success criteria defined collaboratively.

Phase 2 - Regional Rollout (Months 4-9): Expand to 6 sites with full module suite. Includes MES integration and AI module activation.

Phase 3 - Global Completion (Months 10-16): Complete remaining 4 sites with full optimization.

Migration Strategy: Our Zero-Downtime Migration Framework (ZDMF) uses parallel running with intelligent data synchronization. We have executed 47 zero-downtime migrations to date.

Training: Comprehensive training program including:
- 40-hour certification program for system administrators
- Role-based training modules for all 500+ users
- Video library with 200+ training modules
- On-site training at all 12 locations
- Dedicated learning management system for ongoing education

Project Management: Sarah Chen, PMP (15 years experience) will serve as dedicated project manager. Weekly steering committee meetings and real-time project dashboard.

SECTION 4: COMMERCIAL PROPOSAL

Total Investment:
- Implementation cost: $4.2 million (within $5M budget)
- Year 1 maintenance: $420,000 (10% of implementation)
- Years 2-5 maintenance: $380,000/year with capped annual increases of 3%
- 5-Year TCO: $5.76 million

Payment Structure: Milestone-based payments aligned to phase completions:
- Contract signing: 10%
- Pilot completion: 20%
- Regional rollout: 30%
- Global completion: 30%
- 90-day warranty period: 10%

SECTION 5: VENDOR QUALIFICATIONS

Experience: Founded in 2009, TechSolutions has 15 years of ERP implementation experience with 215 successful implementations across manufacturing, retail, and financial services.

Manufacturing References:
1. GlobalAuto Components (Fortune 200) - SAP to cloud migration, 8 sites, completed 2022
2. PrecisionParts International - Full ERP implementation, 15 countries, completed 2023  
3. AeroManufacturing Ltd (Fortune 500) - Greenfield implementation, 20 sites, 2021

Cloud Partnerships: AWS Advanced Partner (since 2015), Microsoft Azure Gold Partner, Google Cloud Partner. All three certifications are current.

Global Presence: Local teams in 10 of 12 target countries. For the remaining 2 countries (Vietnam, Nigeria), we have strategic partnerships with certified local implementation partners.

Quality: ISO 9001:2015 certified since 2012. Annual surveillance audits with no major non-conformities.

SECTION 6: SUPPORT & MAINTENANCE

24/7 Support: Global support center staffed 24/7/365 with 2-hour response SLA for critical (P1) issues, exceeding the 4-hour requirement. P2 issues: 8 hours. P3 issues: 24 hours.

Customer Success: Dedicated customer success manager (CSM) assigned for 18 months post go-live (6 months beyond requirement). Monthly executive business reviews in addition to quarterly health checks.

Continuous Improvement: Quarterly optimization reviews with performance benchmarking and best practice recommendations from our Center of Excellence.
"""

SAMPLE_RFP_2 = """
REQUEST FOR PROPOSAL
AI-Powered Customer Service Platform
RFP-CS-2024-007

OVERVIEW
RetailCo seeks an AI-powered customer service automation platform to handle 80% of customer inquiries without human intervention.

TECHNICAL REQUIREMENTS
- Natural Language Processing with support for English, Spanish, French, German
- Integration with existing CRM (Salesforce) and ticketing system (Zendesk)
- Real-time sentiment analysis and escalation triggers
- 99.5% uptime SLA
- Processing capacity: 10,000 concurrent conversations
- Response time under 2 seconds for 95% of queries

SECURITY & COMPLIANCE
- GDPR and CCPA compliance required
- PCI DSS compliance for payment-related queries
- Data encryption in transit and at rest
- Comprehensive conversation logging for quality assurance

TIMELINE
- Proof of concept within 60 days
- Full production deployment within 6 months
- 24/7 support post-deployment

FINANCIAL
- Budget: $800,000 implementation + ongoing SaaS fees
- ROI demonstration within 12 months

VENDOR REQUIREMENTS  
- Minimum 5 years in conversational AI
- 3 retail sector references required
"""
